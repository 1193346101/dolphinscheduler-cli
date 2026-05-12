"""
Process Definition Operations for DolphinScheduler 3.2.0
Path renamed from workflow-definition to process-definition
Includes workflow_* aliases for compatibility with DS341Adapter
"""
from __future__ import annotations

from dsctl.generated.versions.ds_3_4_1.api.operations._base import BaseRequestsClient, BaseParamsModel

from pydantic import Field, TypeAdapter

from dsctl.generated.versions.ds_3_4_1.common.enums.release_state import ReleaseState
from dsctl.generated.versions.ds_3_4_1.common.enums.workflow_execution_type_enum import WorkflowExecutionTypeEnum
from dsctl.generated.versions.ds_3_4_1.dao.entities.dag_data import DagData
from dsctl.generated.versions.ds_3_4_1.dao.entities.dependent_simplify_definition import DependentSimplifyDefinition
from dsctl.generated.versions.ds_3_4_1.dao.entities.task_definition import TaskDefinition
from dsctl.generated.versions.ds_3_4_1.dao.entities.workflow_definition import WorkflowDefinition
from dsctl.generated.versions.ds_3_4_1.api.contracts.page_info import PageInfoWorkflowDefinition, PageInfoWorkflowDefinitionLog
from dsctl.generated.versions.ds_3_4_1.api.contracts.treeview.tree_view_dto import TreeViewDto
from dsctl.generated.versions.ds_3_4_1.api.views.workflow_definition import WorkflowDefinitionSimpleItem, WorkflowDefinitionVariablesView


class QueryProcessDefinitionListPagingParams(BaseParamsModel):
    searchVal: str | None = Field(default=None, description='search value')
    otherParamsJson: str | None = Field(default=None, description='otherParamsJson')
    userId: int | None = Field(default=None, description='user id', examples=[100])
    pageNo: int = Field(description='page number', examples=[1])
    pageSize: int = Field(description='page size', examples=[10])


class CreateProcessDefinitionParams(BaseParamsModel):
    name: str = Field(description='process definition name')
    description: str | None = Field(default=None)
    globalParams: str | None = Field(default=None)
    locations: str | None = Field(default=None)
    timeout: int | None = Field(default=None)
    taskRelationJson: str = Field(description='relation json for nodes')
    taskDefinitionJson: str = Field(description='taskDefinitionJson')
    otherParamsJson: str | None = Field(default=None)
    executionType: WorkflowExecutionTypeEnum | None = Field(default=None)


class GetTaskListByProcessDefinitionCodeParams(BaseParamsModel):
    processDefinitionCode: int = Field(examples=[100])


class UpdateProcessDefinitionParams(BaseParamsModel):
    name: str = Field(description='process definition name')
    description: str | None = Field(default=None)
    globalParams: str | None = Field(default=None)
    locations: str | None = Field(default=None)
    timeout: int | None = Field(default=None)
    taskRelationJson: str = Field(description='relation json')
    taskDefinitionJson: str = Field(description='taskDefinitionJson')
    executionType: WorkflowExecutionTypeEnum | None = Field(default=None)
    releaseState: ReleaseState | None = Field(default=None)


class ReleaseProcessDefinitionParams(BaseParamsModel):
    releaseState: ReleaseState


class ProcessDefinitionOperations(BaseRequestsClient):
    """Process definition operations for DS 3.2.0 (uses process-definition path)."""

    # === Core process-* methods ===

    def query_process_definition_list_paging(self, project_code: int, params) -> PageInfoWorkflowDefinition:
        path = f"projects/{project_code}/process-definition"
        query_params = self._model_mapping(params)
        payload = self._request("GET", path, params=query_params)
        return self._validate_payload(payload, TypeAdapter(PageInfoWorkflowDefinition))

    def create_process_definition(self, project_code: int, form) -> None:
        path = f"projects/{project_code}/process-definition"
        data = self._model_mapping(form)
        self._request("POST", path, data=data)
        return None

    def query_all_process_definition_by_project_code(self, project_code: int) -> list[DagData]:
        path = f"projects/{project_code}/process-definition/all"
        payload = self._request("GET", path)
        # Transform each item in the list
        if payload and isinstance(payload, list):
            for item in payload:
                if isinstance(item, dict):
                    if "processDefinition" in item:
                        item["workflowDefinition"] = item.pop("processDefinition")
                    if "processTaskRelationList" in item:
                        item["workflowTaskRelationList"] = item.pop("processTaskRelationList")
        return self._validate_payload(payload, TypeAdapter(list[DagData]))

    def query_process_definition_list(self, project_code: int) -> list[DagData]:
        path = f"projects/{project_code}/process-definition/list"
        payload = self._request("GET", path)
        return self._validate_payload(payload, TypeAdapter(list[DagData]))

    def query_process_definition_by_name(self, project_code: int, name: str) -> DagData:
        path = f"projects/{project_code}/process-definition/query-by-name"
        payload = self._request("GET", path, params={"name": name})
        # Transform 3.2.0 keys to 3.4.1 keys for DagData validation
        if payload and isinstance(payload, dict):
            if "processDefinition" in payload:
                payload["workflowDefinition"] = payload.pop("processDefinition")
            if "processTaskRelationList" in payload:
                payload["workflowTaskRelationList"] = payload.pop("processTaskRelationList")
        return self._validate_payload(payload, TypeAdapter(DagData))

    def get_task_list_by_process_definition_code(self, project_code: int, params) -> list[DependentSimplifyDefinition]:
        path = f"projects/{project_code}/process-definition/query-task-definition-list"
        query_params = self._model_mapping(params)
        payload = self._request("GET", path, params=query_params)
        return self._validate_payload(payload, TypeAdapter(list[DependentSimplifyDefinition]))

    def get_process_list_by_project_code(self, project_code: int) -> list[DependentSimplifyDefinition]:
        path = f"projects/{project_code}/process-definition/query-process-definition-list"
        payload = self._request("GET", path)
        return self._validate_payload(payload, TypeAdapter(list[DependentSimplifyDefinition]))

    def delete_process_definition_by_code(self, project_code: int, code: int) -> None:
        path = f"projects/{project_code}/process-definition/{code}"
        self._request("DELETE", path)
        return None

    def query_process_definition_by_code(self, project_code: int, code: int) -> DagData:
        path = f"projects/{project_code}/process-definition/{code}"
        payload = self._request("GET", path)
        # Transform 3.2.0 keys to 3.4.1 keys for DagData validation
        if payload and isinstance(payload, dict):
            if "processDefinition" in payload:
                payload["workflowDefinition"] = payload.pop("processDefinition")
            if "processTaskRelationList" in payload:
                payload["workflowTaskRelationList"] = payload.pop("processTaskRelationList")
        return self._validate_payload(payload, TypeAdapter(DagData))

    def update_process_definition(self, project_code: int, code: int, form) -> None:
        path = f"projects/{project_code}/process-definition/{code}"
        data = self._model_mapping(form)
        self._request("PUT", path, data=data)
        return None

    def release_process_definition(self, project_code: int, code: int, form) -> bool:
        path = f"projects/{project_code}/process-definition/{code}/release"
        data = self._model_mapping(form)
        payload = self._request("POST", path, data=data)
        # DS 3.2.0 returns null on success, return True for successful release
        if payload is None:
            return True
        return self._validate_payload(payload, TypeAdapter(bool))

    def get_node_list_by_definition_code(self, project_code: int, code: int) -> list[TaskDefinition]:
        path = f"projects/{project_code}/process-definition/{code}/tasks"
        payload = self._request("GET", path)
        return self._validate_payload(payload, TypeAdapter(list[TaskDefinition]))

    def view_tree(self, project_code: int, code: int, limit: int = 100) -> TreeViewDto:
        path = f"projects/{project_code}/process-definition/{code}/view-tree"
        payload = self._request("GET", path, params={"limit": limit})
        return self._validate_payload(payload, TypeAdapter(TreeViewDto))

    def view_variables(self, project_code: int, code: int) -> WorkflowDefinitionVariablesView:
        path = f"projects/{project_code}/process-definition/{code}/view-variables"
        payload = self._request("GET", path)
        return self._validate_payload(payload, TypeAdapter(WorkflowDefinitionVariablesView))

    # === Workflow-* aliases for DS341Adapter compatibility ===

    def query_workflow_definition_list_paging(self, project_code: int, params):
        return self.query_process_definition_list_paging(project_code, params)

    def create_workflow_definition(self, project_code: int, form):
        return self.create_process_definition(project_code, form)

    def query_workflow_definition_by_code(self, project_code: int, code: int) -> DagData:
        return self.query_process_definition_by_code(project_code, code)

    def query_workflow_definition_by_name(self, project_code: int, name: str) -> DagData:
        return self.query_process_definition_by_name(project_code, name)

    def update_workflow_definition(self, project_code: int, code: int, form):
        return self.update_process_definition(project_code, code, form)

    def delete_workflow_definition_by_code(self, project_code: int, code: int):
        return self.delete_process_definition_by_code(project_code, code)

    def release_workflow_definition(self, project_code: int, code: int, form) -> bool:
        return self.release_process_definition(project_code, code, form)

    def get_task_list_by_workflow_definition_code(self, project_code: int, params):
        return self.get_task_list_by_process_definition_code(project_code, params)

    def get_workflow_list_by_project_code(self, project_code: int) -> list[DependentSimplifyDefinition]:
        return self.get_process_list_by_project_code(project_code)

    def query_all_workflow_definition_by_project_code(self, project_code: int) -> list[DagData]:
        return self.query_all_process_definition_by_project_code(project_code)


__all__ = ["ProcessDefinitionOperations"]