"""
Executor Operations for DolphinScheduler 3.2.0
Path and parameter names changed from workflow to process
Includes workflow_* aliases for compatibility with DS341Adapter
"""
from __future__ import annotations

from dsctl.generated.versions.ds_3_4_1.api.operations._base import BaseRequestsClient, BaseParamsModel

from pydantic import Field, TypeAdapter

from dsctl.generated.versions.ds_3_4_1.common.enums.command_type import CommandType
from dsctl.generated.versions.ds_3_4_1.common.enums.complement_dependent_mode import ComplementDependentMode
from dsctl.generated.versions.ds_3_4_1.common.enums.execution_order import ExecutionOrder
from dsctl.generated.versions.ds_3_4_1.common.enums.failure_strategy import FailureStrategy
from dsctl.generated.versions.ds_3_4_1.common.enums.priority import Priority
from dsctl.generated.versions.ds_3_4_1.common.enums.run_mode import RunMode
from dsctl.generated.versions.ds_3_4_1.common.enums.task_depend_type import TaskDependType
from dsctl.generated.versions.ds_3_4_1.common.enums.warning_type import WarningType
from dsctl.generated.versions.ds_3_4_1.api.enums.execute_type import ExecuteType


class TriggerProcessDefinitionParams(BaseParamsModel):
    """Start Process Instance - DS 3.2.0 uses processDefinitionCode."""
    processDefinitionCode: int = Field(description='process definition code', examples=[100])
    scheduleTime: str = Field(description='schedule time', examples=['2022-04-06 00:00:00,2022-04-06 00:00:00'])
    failureStrategy: FailureStrategy = Field(description='failure strategy')
    startNodeList: str | None = Field(default=None, description='start nodes list')
    taskDependType: TaskDependType | None = Field(default=None, description='task depend type')
    execType: CommandType | None = Field(default=None, description='execute type')
    warningType: WarningType = Field(description='warning type')
    warningGroupId: int | None = Field(default=None, description='warning group id', examples=[100])
    runMode: RunMode | None = Field(default=None, description='run mode')
    processInstancePriority: Priority | None = Field(default=None, description='process instance priority')
    workerGroup: str | None = Field(default=None, description='worker group', examples=['default'])
    tenantCode: str | None = Field(default=None, description='tenant code', examples=['default'])
    environmentCode: int | None = Field(default=None, examples=[-1])
    startParams: str | None = Field(default=None)
    expectedParallelismNumber: int | None = Field(default=None, examples=[8])
    dryRun: int | None = Field(default=None, examples=[0])
    complementDependentMode: ComplementDependentMode | None = Field(default=None)
    allLevelDependent: bool | None = Field(default=None, examples=[False])
    executionOrder: ExecutionOrder | None = Field(default=None)


class ControlProcessInstanceParams(BaseParamsModel):
    """Execute - DS 3.2.0 uses processInstanceId."""
    processInstanceId: int = Field(examples=[100])
    executeType: ExecuteType


class ExecuteTaskParams(BaseParamsModel):
    """Execute Task."""
    processInstanceId: int = Field(description='process instance id', examples=[100])
    startNodeList: str = Field(description='start node list')
    taskDependType: TaskDependType = Field(description='task depend type')


class ExecutorOperations(BaseRequestsClient):
    """Executor operations for DS 3.2.0 (uses process-* endpoints)."""

    # === Core process-* methods ===

    def trigger_process_definition(self, project_code: int, form: TriggerProcessDefinitionParams) -> list[int]:
        """Start process instance - DS 3.2.0 endpoint."""
        path = f"projects/{project_code}/executors/start-process-instance"
        data = self._model_mapping(form)
        payload = self._request("POST", path, data=data)
        # DS 3.2.0 returns a single int (process instance code), convert to list
        if isinstance(payload, int):
            return [payload]
        return self._validate_payload(payload, TypeAdapter(list[int]))

    def control_process_instance(self, project_code: int, form: ControlProcessInstanceParams) -> None:
        """Execute process instance action."""
        path = f"projects/{project_code}/executors/execute"
        data = self._model_mapping(form)
        self._request("POST", path, data=data)
        return None

    def execute_task(self, project_code: int, form: ExecuteTaskParams) -> None:
        """Execute task from specific node."""
        path = f"projects/{project_code}/executors/execute-task"
        data = self._model_mapping(form)
        self._request("POST", path, data=data)
        return None

    # === Workflow-* aliases for DS341Adapter compatibility ===

    def trigger_workflow_definition(self, project_code: int, form) -> list[int]:
        """Alias for trigger_process_definition with param conversion."""
        if hasattr(form, 'workflowDefinitionCode'):
            params = TriggerProcessDefinitionParams(
                processDefinitionCode=form.workflowDefinitionCode,
                scheduleTime=form.scheduleTime,
                failureStrategy=form.failureStrategy,
                startNodeList=form.startNodeList,
                taskDependType=form.taskDependType,
                execType=form.execType,
                warningType=form.warningType,
                warningGroupId=form.warningGroupId,
                runMode=form.runMode,
                processInstancePriority=form.workflowInstancePriority,
                workerGroup=form.workerGroup,
                tenantCode=form.tenantCode,
                environmentCode=form.environmentCode,
                startParams=form.startParams,
                expectedParallelismNumber=form.expectedParallelismNumber,
                dryRun=form.dryRun,
                complementDependentMode=form.complementDependentMode,
                allLevelDependent=form.allLevelDependent,
                executionOrder=form.executionOrder,
            )
            return self.trigger_process_definition(project_code, params)
        return self.trigger_process_definition(project_code, form)

    def control_workflow_instance(self, project_code: int, form) -> None:
        """Alias for control_process_instance with param conversion."""
        if hasattr(form, 'workflowInstanceId'):
            params = ControlProcessInstanceParams(
                processInstanceId=form.workflowInstanceId,
                executeType=form.executeType,
            )
            return self.control_process_instance(project_code, params)
        return self.control_process_instance(project_code, form)


__all__ = ["ExecutorOperations"]