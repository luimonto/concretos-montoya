from decimal import Decimal

from django.db.models import Sum
from django.shortcuts import render
from django.utils import timezone

from project.models import Project, Requisition


def dashboard(request):

    today = timezone.localdate()

    active_projects = (
        Project.objects
        .filter(
            active=True,
            status__in=[
                Project.Status.PLANNED,
                Project.Status.IN_PROGRESS,
            ],
        )
        .select_related("client")
        .prefetch_related(
            "expenses",
            "requisitions",
        )
        .order_by("estimated_end_date")
    )

    total_budget = Decimal("0.00")
    total_spent = Decimal("0.00")
    total_committed = Decimal("0.00")

    for project in active_projects:

        # ==================================================
        # MONEY
        # ==================================================

        spent = (
            project.expenses.aggregate(
                total=Sum("amount")
            )["total"]
            or Decimal("0.00")
        )

        committed = (
            project.requisitions
            .filter(
                status=Requisition.Status.APPROVED
            )
            .aggregate(
                total=Sum("estimated_total")
            )["total"]
            or Decimal("0.00")
        )

        project.spent = spent
        project.committed = committed

        project.available = (
            project.budget - spent
        )

        # Porcentaje del presupuesto que ya se gastó
        if project.budget > 0:
            project.money_progress = min(
                round(
                    (spent / project.budget) * 100
                ),
                100,
            )
        else:
            project.money_progress = 0

        total_budget += project.budget
        total_spent += spent
        total_committed += committed

        # ==================================================
        # TIME PROGRESS
        # ==================================================

        if (
            project.start_date
            and project.estimated_end_date
        ):

            total_days = (
                project.estimated_end_date
                - project.start_date
            ).days

            elapsed_days = (
                today - project.start_date
            ).days

            if total_days > 0:
                project.time_progress = max(
                    0,
                    min(
                        100,
                        round(
                            (
                                elapsed_days
                                / total_days
                            ) * 100
                        ),
                    ),
                )
            else:
                project.time_progress = 100

        else:
            project.time_progress = None

        # ==================================================
        # SCHEDULE STATUS
        # ==================================================

        if (
            project.estimated_end_date
            and project.estimated_end_date < today
        ):
            project.schedule_status = "overdue"

        elif (
            project.estimated_end_date
            and (
                project.estimated_end_date - today
            ).days <= 14
        ):
            project.schedule_status = "warning"

        else:
            project.schedule_status = "on_time"

        # ==================================================
        # FINANCIAL STATUS
        # ==================================================

        if (
            project.time_progress is not None
            and project.money_progress
            > project.time_progress + 25
        ):
            project.financial_status = "critical"

        elif (
            project.time_progress is not None
            and project.money_progress
            > project.time_progress + 10
        ):
            project.financial_status = "warning"

        else:
            project.financial_status = "on_track"

    # ==================================================
    # COUNTERS
    # ==================================================

    total_active = active_projects.count()

    planned_count = active_projects.filter(
        status=Project.Status.PLANNED
    ).count()

    in_progress_count = active_projects.filter(
        status=Project.Status.IN_PROGRESS
    ).count()

    overdue_count = sum(
        1
        for project in active_projects
        if project.schedule_status == "overdue"
    )

    return render(
        request,
        "projects/dashboard.html",
        {
            "active_projects": active_projects,

            "total_active": total_active,

            "planned_count": planned_count,

            "in_progress_count": in_progress_count,

            "overdue_count": overdue_count,

            "total_budget": total_budget,

            "total_spent": total_spent,

            "total_committed": total_committed,

            "total_available": (
                total_budget - total_spent
            ),
        },
    )