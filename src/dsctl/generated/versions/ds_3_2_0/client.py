"""
DolphinScheduler 3.2.0 Client
Reuses most operations from 3.4.1, replaces process-* endpoints
"""
from __future__ import annotations

from dsctl.generated.versions.ds_3_4_1.api.operations._base import SessionLike
from pydantic import TypeAdapter

# Import 3.2.0 specific operations
from .api.operations.process_definition import ProcessDefinitionOperations
from .api.operations.process_instance import ProcessInstanceOperations, _convert_dag_data_fields
from .api.operations.executor import ExecutorOperations
from .api.operations.task_instance import TaskInstanceOperations

# Reuse other operations from 3.4.1 (no API changes)
from dsctl.generated.versions.ds_3_4_1.api.operations.access_token import AccessTokenOperations
from dsctl.generated.versions.ds_3_4_1.api.operations.alert_group import AlertGroupOperations
from dsctl.generated.versions.ds_3_4_1.api.operations.alert_plugin_instance import AlertPluginInstanceOperations
from dsctl.generated.versions.ds_3_4_1.api.operations.audit_log import AuditLogOperations
from dsctl.generated.versions.ds_3_4_1.api.operations.cluster import ClusterOperations
from dsctl.generated.versions.ds_3_4_1.api.operations.data_source import DataSourceOperations
from dsctl.generated.versions.ds_3_4_1.api.operations.environment import EnvironmentOperations
from dsctl.generated.versions.ds_3_4_1.api.operations.k8s_namespace import K8sNamespaceOperations
from dsctl.generated.versions.ds_3_4_1.api.operations.logger import LoggerOperations
from dsctl.generated.versions.ds_3_4_1.api.operations.monitor import MonitorOperations
from dsctl.generated.versions.ds_3_4_1.api.operations.project import ProjectOperations
from dsctl.generated.versions.ds_3_4_1.api.operations.project_parameter import ProjectParameterOperations
from dsctl.generated.versions.ds_3_4_1.api.operations.project_preference import ProjectPreferenceOperations
from dsctl.generated.versions.ds_3_4_1.api.operations.queue import QueueOperations
from dsctl.generated.versions.ds_3_4_1.api.operations.resources import ResourcesOperations
from dsctl.generated.versions.ds_3_4_1.api.operations.scheduler import SchedulerOperations
from dsctl.generated.versions.ds_3_4_1.api.operations.task_definition import TaskDefinitionOperations
from dsctl.generated.versions.ds_3_4_1.api.operations.task_group import TaskGroupOperations
from dsctl.generated.versions.ds_3_4_1.api.operations.tenant import TenantOperations
from dsctl.generated.versions.ds_3_4_1.api.operations.users import UsersOperations
from dsctl.generated.versions.ds_3_4_1.api.operations.worker_group import WorkerGroupOperations
from dsctl.generated.versions.ds_3_4_1.api.operations.workflow_lineage import WorkflowLineageOperations
from dsctl.generated.versions.ds_3_4_1.api.operations.workflow_task_relation import WorkflowTaskRelationOperations
from dsctl.generated.versions.ds_3_4_1.api.operations.workflow_v2 import WorkflowV2Operations
from dsctl.generated.versions.ds_3_4_1.api.operations.workflow_instance_v2 import WorkflowInstanceV2Operations
from dsctl.generated.versions.ds_3_4_1.api.operations.task_instance_v2 import TaskInstanceV2Operations

# Import entities for type adapter
from dsctl.generated.versions.ds_3_4_1.dao.entities.workflow_instance import WorkflowInstance


class DS320WorkflowInstanceV2Operations(WorkflowInstanceV2Operations):
    """Workflow instance v2 operations for DS 3.2.0 with field mapping."""

    def query_workflow_instance_by_id(self, workflow_instance_id: int) -> WorkflowInstance:
        """Query workflow instance by id with field name conversion for DS 3.2.0."""
        path = f"v2/workflow-instances/{workflow_instance_id}"
        payload = self._request("GET", path)
        # Convert field names for DS 3.2.0
        _convert_dag_data_fields(payload)
        return self._validate_payload(payload, TypeAdapter(WorkflowInstance))


class DS320Client:
    """Client for DolphinScheduler 3.2.0 API."""

    def __init__(
        self,
        base_url: str,
        token: str,
        *,
        session: SessionLike | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.token = token
        self._session = session

        # 3.2.0 specific operations (process-* endpoints)
        self.process_definition = ProcessDefinitionOperations(
            self.base_url, self.token, session=self._session
        )
        self.process_instance = ProcessInstanceOperations(
            self.base_url, self.token, session=self._session
        )
        self.executor = ExecutorOperations(
            self.base_url, self.token, session=self._session
        )

        # Reused operations from 3.4.1 (unchanged API)
        self.access_token = AccessTokenOperations(
            self.base_url, self.token, session=self._session
        )
        self.alert_group = AlertGroupOperations(
            self.base_url, self.token, session=self._session
        )
        self.alert_plugin_instance = AlertPluginInstanceOperations(
            self.base_url, self.token, session=self._session
        )
        self.audit_log = AuditLogOperations(
            self.base_url, self.token, session=self._session
        )
        self.cluster = ClusterOperations(
            self.base_url, self.token, session=self._session
        )
        self.data_source = DataSourceOperations(
            self.base_url, self.token, session=self._session
        )
        self.environment = EnvironmentOperations(
            self.base_url, self.token, session=self._session
        )
        self.k8s_namespace = K8sNamespaceOperations(
            self.base_url, self.token, session=self._session
        )
        self.logger = LoggerOperations(
            self.base_url, self.token, session=self._session
        )
        self.monitor = MonitorOperations(
            self.base_url, self.token, session=self._session
        )
        self.project = ProjectOperations(
            self.base_url, self.token, session=self._session
        )
        self.project_parameter = ProjectParameterOperations(
            self.base_url, self.token, session=self._session
        )
        self.project_preference = ProjectPreferenceOperations(
            self.base_url, self.token, session=self._session
        )
        self.queue = QueueOperations(
            self.base_url, self.token, session=self._session
        )
        self.resources = ResourcesOperations(
            self.base_url, self.token, session=self._session
        )
        self.scheduler = SchedulerOperations(
            self.base_url, self.token, session=self._session
        )
        self.task_definition = TaskDefinitionOperations(
            self.base_url, self.token, session=self._session
        )
        self.task_group = TaskGroupOperations(
            self.base_url, self.token, session=self._session
        )
        self.task_instance = TaskInstanceOperations(
            self.base_url, self.token, session=self._session
        )
        self.tenant = TenantOperations(
            self.base_url, self.token, session=self._session
        )
        self.users = UsersOperations(
            self.base_url, self.token, session=self._session
        )
        self.worker_group = WorkerGroupOperations(
            self.base_url, self.token, session=self._session
        )
        self.workflow_lineage = WorkflowLineageOperations(
            self.base_url, self.token, session=self._session
        )
        self.workflow_task_relation = WorkflowTaskRelationOperations(
            self.base_url, self.token, session=self._session
        )
        self.workflow_v2 = WorkflowV2Operations(
            self.base_url, self.token, session=self._session
        )
        # Use DS 3.2.0 specific workflow_instance_v2 with field mapping
        self.workflow_instance_v2 = DS320WorkflowInstanceV2Operations(
            self.base_url, self.token, session=self._session
        )
        self.task_instance_v2 = TaskInstanceV2Operations(
            self.base_url, self.token, session=self._session
        )

        # Alias for compatibility with adapter
        self.workflow_definition = self.process_definition
        self.workflow_instance = self.process_instance
        # 3.2.0 doesn't have /v2/projects API, use regular /project
        self.project_v2 = self.project


__all__ = ["DS320Client"]