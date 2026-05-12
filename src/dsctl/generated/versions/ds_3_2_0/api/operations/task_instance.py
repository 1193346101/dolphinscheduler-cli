"""
Task Instance Operations for DolphinScheduler 3.2.0
Uses processInstanceId instead of workflowInstanceId
"""
from __future__ import annotations

from dsctl.generated.versions.ds_3_4_1.api.operations._base import BaseRequestsClient, BaseParamsModel

from pydantic import Field, TypeAdapter

from dsctl.generated.versions.ds_3_4_1.common.enums.task_execute_type import TaskExecuteType
from dsctl.generated.versions.ds_3_4_1.plugin.task_api.enums.task_execution_status import TaskExecutionStatus
from dsctl.generated.versions.ds_3_4_1.api.contracts.page_info import PageInfoTaskInstance


class QueryProcessTaskListPagingParams(BaseParamsModel):
    """Query Task List Paging - DS 3.2.0 uses processInstanceId."""
    processInstanceId: int | None = Field(default=None, description='process instance id', examples=[100])
    processInstanceName: str | None = Field(default=None)
    processDefinitionName: str | None = Field(default=None)
    searchVal: str | None = Field(default=None, description='search value')
    taskName: str | None = Field(default=None, description='task name')
    taskCode: int | None = Field(default=None)
    executorName: str | None = Field(default=None)
    stateType: TaskExecutionStatus | None = Field(default=None, description='state type')
    host: str | None = Field(default=None, description='host')
    startDate: str | None = Field(default=None, description='start time')
    endDate: str | None = Field(default=None, description='end time')
    taskExecuteType: TaskExecuteType | None = Field(default=None, description='task execute type', examples=['STREAM'])
    pageNo: int = Field(description='page number', examples=[1])
    pageSize: int = Field(description='page size', examples=[20])


class TaskInstanceOperations(BaseRequestsClient):
    """Task instance operations for DS 3.2.0."""

    def query_task_list_paging(
        self,
        project_code: int,
        params
    ) -> PageInfoTaskInstance:
        """Query task list paging - handles both workflow and process param names."""
        path = f"projects/{project_code}/task-instances"

        # Convert workflow params to process params if needed
        if hasattr(params, 'workflowInstanceId'):
            converted = QueryProcessTaskListPagingParams(
                processInstanceId=params.workflowInstanceId,
                processInstanceName=params.workflowInstanceName if hasattr(params, 'workflowInstanceName') else None,
                processDefinitionName=params.workflowDefinitionName if hasattr(params, 'workflowDefinitionName') else None,
                searchVal=params.searchVal if hasattr(params, 'searchVal') else None,
                taskName=params.taskName if hasattr(params, 'taskName') else None,
                taskCode=params.taskCode if hasattr(params, 'taskCode') else None,
                executorName=params.executorName if hasattr(params, 'executorName') else None,
                stateType=params.stateType if hasattr(params, 'stateType') else None,
                host=params.host if hasattr(params, 'host') else None,
                startDate=params.startDate if hasattr(params, 'startDate') else None,
                endDate=params.endDate if hasattr(params, 'endDate') else None,
                taskExecuteType=params.taskExecuteType if hasattr(params, 'taskExecuteType') else None,
                pageNo=params.pageNo,
                pageSize=params.pageSize,
            )
            query_params = self._model_mapping(converted)
        else:
            query_params = self._model_mapping(params)

        payload = self._request("GET", path, params=query_params)
        return self._validate_payload(payload, TypeAdapter(PageInfoTaskInstance))


__all__ = ["TaskInstanceOperations"]