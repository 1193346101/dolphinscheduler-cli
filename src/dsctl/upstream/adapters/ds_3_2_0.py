"""
DolphinScheduler 3.2.0 Adapter
Uses process-* endpoints and /projects API (no /v2/projects)
"""
from __future__ import annotations

import httpx
from dataclasses import dataclass
from typing import TYPE_CHECKING, cast

from dsctl.generated.versions.ds_3_2_0 import DS320Client
from dsctl.generated.versions.ds_3_4_1.api.operations._base import SessionLike
from dsctl.generated.versions.ds_3_4_1.api.operations.project import (
    QueryProjectListPagingParams,
    CreateProjectParams,
    UpdateProjectParams,
)
from dsctl.generated.versions.ds_3_4_1.dao.entities.project import Project
from dsctl.generated.versions.ds_3_4_1.api.contracts.page_info import PageInfoProject
from dsctl.generated.versions.ds_3_4_1.common.enums.priority import Priority
from dsctl.generated.versions.ds_3_4_1.common.enums.failure_strategy import FailureStrategy
from dsctl.generated.versions.ds_3_4_1.common.enums.warning_type import WarningType
from dsctl.generated.versions.ds_3_4_1.common.enums.run_mode import RunMode
from dsctl.generated.versions.ds_3_4_1.common.enums.task_depend_type import TaskDependType
from dsctl.generated.versions.ds_3_4_1.common.enums.command_type import CommandType
from dsctl.generated.versions.ds_3_4_1.common.enums.complement_dependent_mode import ComplementDependentMode
from dsctl.generated.versions.ds_3_4_1.common.enums.execution_order import ExecutionOrder
from dsctl.generated.versions.ds_3_4_1.common.enums.release_state import ReleaseState
from dsctl.upstream.adapters.ds_3_4_1 import (
    DS341Adapter,
    _DS341Session,
    _GeneratedSessionAdapter,
    _DS341TaskTypeOperations,
    _DS341ProjectParameterOperations,
    _DS341ProjectPreferenceOperations,
    _DS341ProjectWorkerGroupOperations,
    _DS341AccessTokenOperations,
    _DS341ClusterOperations,
    _DS341EnvironmentOperations,
    _DS341DataSourceOperations,
    _DS341NamespaceOperations,
    _DS341UiPluginOperations,
    _DS341AlertPluginOperations,
    _DS341AlertGroupOperations,
    _DS341QueueOperations,
    _DS341WorkerGroupOperations,
    _DS341TaskGroupOperations,
    _DS341TenantOperations,
    _DS341UserOperations,
    _DS341AuditOperations,
    _DS341MonitorOperations,
    _DS341ResourceOperations,
    _DS341TaskOperations,
    _DS341WorkflowLineageOperations,
    _DS341ScheduleOperations,
    _DS341WorkflowOperations,
    _DS341WorkflowInstanceOperations,
    _DS341TaskInstanceOperations,
)
from dsctl.upstream.protocol import UpstreamAdapter, ProjectOperations
from dsctl.config import ClusterProfile
from dsctl.client import DolphinSchedulerClient

if TYPE_CHECKING:
    from dsctl.generated.versions.ds_3_4_1.dao.entities.dag_data import DagData
    from dsctl.generated.versions.ds_3_4_1.dao.entities.dependent_simplify_definition import DependentSimplifyDefinition


@dataclass(frozen=True)
class _DS320ProjectOperations:
    """Project operations using /projects API (3.2.0 has no /v2/projects)."""

    client: DS320Client

    def list(
        self,
        *,
        page_no: int,
        page_size: int,
        search: str | None = None,
    ) -> PageInfoProject:
        return self.client.project.query_project_list_paging(
            QueryProjectListPagingParams(
                searchVal=search,
                pageNo=page_no,
                pageSize=page_size,
            )
        )

    def get(self, *, code: int) -> Project:
        return self.client.project.query_project_by_code(code)

    def create(self, *, name: str, description: str | None = None) -> Project:
        return self.client.project.create_project(
            CreateProjectParams(
                projectName=name,
                description=description,
            )
        )

    def update(
        self,
        *,
        code: int,
        name: str,
        description: str | None = None,
    ) -> Project:
        return self.client.project.update_project(
            code,
            UpdateProjectParams(
                projectName=name,
                description=description,
            ),
        )

    def delete(self, *, code: int) -> bool:
        self.client.project.delete_project(code)
        return True


@dataclass(frozen=True)
class _DS320Session(_DS341Session):
    """Session for DS 3.2.0 with process-* endpoints."""

    # Override projects to use /projects API
    projects: ProjectOperations


class DS320Adapter(DS341Adapter):
    """Adapter for DolphinScheduler 3.2.0."""

    ds_version: str = "3.2.0"
    version_slug: str = "ds_3_2_0"
    client_class: type[DS320Client] = DS320Client

    def create_client(
        self,
        profile: ClusterProfile,
        *,
        transport: "httpx.BaseTransport | None" = None,
        client: "DolphinSchedulerClient | None" = None,
    ) -> DS320Client:
        if client is not None and transport is not None:
            raise ValueError("create_client() accepts either transport or client")
        transport_client = client or DolphinSchedulerClient(profile, transport=transport)
        generated_session = cast(
            "SessionLike",
            _GeneratedSessionAdapter(transport_client, base_url=profile.api_url),
        )
        return DS320Client(profile.api_url, profile.api_token, session=generated_session)

    def bind(
        self,
        profile: ClusterProfile,
        *,
        http_client: DolphinSchedulerClient,
    ) -> _DS320Session:
        """Bind 3.2.0 operations."""
        client = self.create_client(profile, client=http_client)
        return _DS320Session(
            task_types=_DS341TaskTypeOperations(client=client),
            projects=_DS320ProjectOperations(client=client),  # Use /projects API
            project_parameters=_DS341ProjectParameterOperations(client=client),
            project_preferences=_DS341ProjectPreferenceOperations(client=client, http_client=http_client),
            project_worker_groups=_DS341ProjectWorkerGroupOperations(client=client, http_client=http_client),
            access_tokens=_DS341AccessTokenOperations(client=client),
            clusters=_DS341ClusterOperations(client=client),
            environments=_DS341EnvironmentOperations(client=client),
            datasources=_DS341DataSourceOperations(client=client),
            namespaces=_DS341NamespaceOperations(client=client),
            ui_plugins=_DS341UiPluginOperations(client=client),
            alert_plugins=_DS341AlertPluginOperations(client=client),
            alert_groups=_DS341AlertGroupOperations(client=client),
            queues=_DS341QueueOperations(client=client),
            worker_groups=_DS341WorkerGroupOperations(client=client),
            task_groups=_DS341TaskGroupOperations(client=client),
            tenants=_DS341TenantOperations(client=client),
            users=_DS341UserOperations(client=client),
            audits=_DS341AuditOperations(client=client),
            monitor=_DS341MonitorOperations(client=client),
            resources=_DS341ResourceOperations(client=client, http_client=http_client),
            schedules=_DS341ScheduleOperations(client=client),
            tasks=_DS341TaskOperations(client=client),
            workflows=_DS341WorkflowOperations(client=client),
            workflow_instances=_DS341WorkflowInstanceOperations(client=client),
            task_instances=_DS341TaskInstanceOperations(client=client),
            workflow_lineages=_DS341WorkflowLineageOperations(client=client),
        )


DS320_ADAPTER = DS320Adapter()

__all__ = ["DS320Adapter", "DS320_ADAPTER"]