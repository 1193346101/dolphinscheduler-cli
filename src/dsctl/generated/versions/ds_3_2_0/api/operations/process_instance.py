"""
Process Instance Operations for DolphinScheduler 3.2.0
Path changed from workflow-instance to process-instance
Includes workflow_* aliases for compatibility with DS341Adapter
"""
from __future__ import annotations

from dsctl.generated.versions.ds_3_4_1.api.operations._base import BaseRequestsClient, BaseParamsModel

from pydantic import Field, TypeAdapter

from dsctl.generated.versions.ds_3_4_1.dao.entities.workflow_instance import WorkflowInstance
from dsctl.generated.versions.ds_3_4_1.dao.entities.workflow_definition import WorkflowDefinition
from dsctl.generated.versions.ds_3_4_1.api.contracts.page_info import PageInfoWorkflowInstance


class QueryProcessInstanceListParams(BaseParamsModel):
    processDefinitionCode: int | None = Field(default=None)
    searchVal: str | None = Field(default=None)
    executorName: str | None = Field(default=None)
    state: int | None = Field(default=None)
    host: str | None = Field(default=None)
    startDate: str | None = Field(default=None)
    endDate: str | None = Field(default=None)
    pageNo: int = Field(default=1)
    pageSize: int = Field(default=10)


class UpdateProcessInstanceParams(BaseParamsModel):
    taskRelationJson: str = Field(description='relation json')
    taskDefinitionJson: str = Field(description='task definition json')
    locations: str | None = Field(default=None)
    scheduleTime: str | None = Field(default=None)


def _convert_dag_data_fields(payload: dict) -> dict:
    """Convert DS 3.2.0 field names to DS 3.4.1 expected names."""
    # Convert top-level workflow-related fields
    if "processDefinitionCode" in payload:
        payload["workflowDefinitionCode"] = payload["processDefinitionCode"]
    if "processDefinitionVersion" in payload:
        payload["workflowDefinitionVersion"] = payload["processDefinitionVersion"]
    if "processDefinitionName" in payload:
        payload["workflowDefinitionName"] = payload["processDefinitionName"]

    # Convert dagData fields
    if "dagData" in payload and payload["dagData"]:
        dag_data = payload["dagData"]
        # Convert processDefinition -> workflowDefinition
        if "processDefinition" in dag_data:
            dag_data["workflowDefinition"] = dag_data.pop("processDefinition")
        # Convert processTaskRelationList -> workflowTaskRelationList
        if "processTaskRelationList" in dag_data:
            dag_data["workflowTaskRelationList"] = dag_data.pop("processTaskRelationList")
    return payload


class ProcessInstanceOperations(BaseRequestsClient):
    """Process instance operations for DS 3.2.0."""

    # === Core process-* methods ===

    def query_process_instance_list(self, project_code: int, params) -> PageInfoWorkflowInstance:
        path = f"projects/{project_code}/process-instances"
        query_params = self._model_mapping(params)
        payload = self._request("GET", path, params=query_params)
        # Convert field names for each item
        if "totalList" in payload and payload["totalList"]:
            for item in payload["totalList"]:
                _convert_dag_data_fields(item)
        return self._validate_payload(payload, TypeAdapter(PageInfoWorkflowInstance))

    def query_process_instance_by_id(self, project_code: int, process_instance_id: int) -> WorkflowInstance:
        path = f"projects/{project_code}/process-instances/{process_instance_id}"
        payload = self._request("GET", path)
        # Convert field names
        _convert_dag_data_fields(payload)
        return self._validate_payload(payload, TypeAdapter(WorkflowInstance))

    def update_process_instance(self, project_code: int, process_instance_id: int, form) -> WorkflowDefinition:
        """Update process instance and return WorkflowDefinition from dagData.

        Note: DS 3.2.0 returns updated WorkflowInstance, but DS 3.4.1 update returns WorkflowDefinition.
        This method extracts workflowDefinition from dagData to match DS 3.4.1 behavior.
        """
        path = f"projects/{project_code}/process-instances/{process_instance_id}"
        data = self._model_mapping(form)
        payload = self._request("PUT", path, data=data)
        # Convert field names
        _convert_dag_data_fields(payload)
        # Extract workflowDefinition from dagData to match DS 3.4.1 return type
        if "dagData" in payload and payload["dagData"]:
            workflow_def = payload["dagData"].get("workflowDefinition")
            if workflow_def:
                return self._validate_payload(workflow_def, TypeAdapter(WorkflowDefinition))
        # Fallback: validate the full payload as WorkflowInstance and wrap it
        instance = self._validate_payload(payload, TypeAdapter(WorkflowInstance))
        # Return a mock WorkflowDefinition with essential fields
        return WorkflowDefinition(
            code=instance.workflowDefinitionCode or 0,
            name=None,
            version=instance.workflowDefinitionVersion or 0,
        )

    # === Workflow-* aliases for DS341Adapter compatibility ===

    def query_workflow_instance_list(self, project_code: int, params) -> PageInfoWorkflowInstance:
        # Convert workflow params to process params if needed
        if hasattr(params, 'workflowDefinitionCode'):
            # DS341 uses stateType, DS320 uses state (int)
            state_value = None
            if hasattr(params, 'stateType') and params.stateType is not None:
                # Convert WorkflowExecutionStatus enum to int if needed
                state_value = params.stateType.value if hasattr(params.stateType, 'value') else params.stateType
            converted = QueryProcessInstanceListParams(
                processDefinitionCode=params.workflowDefinitionCode,
                searchVal=params.searchVal,
                executorName=params.executorName,
                state=state_value,
                host=params.host,
                startDate=params.startDate,
                endDate=params.endDate,
                pageNo=params.pageNo,
                pageSize=params.pageSize,
            )
            return self.query_process_instance_list(project_code, converted)
        return self.query_process_instance_list(project_code, params)

    def query_workflow_instance_by_id(self, project_code: int, workflow_instance_id: int) -> WorkflowInstance:
        return self.query_process_instance_by_id(project_code, workflow_instance_id)

    def update_workflow_instance(self, project_code: int, workflow_instance_id: int, form) -> WorkflowDefinition:
        return self.update_process_instance(project_code, workflow_instance_id, form)


__all__ = ["ProcessInstanceOperations"]