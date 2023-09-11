# SPDX-License-Identifier: Apache-2.0

from typing import *

# from ..types import *

# from ..op_util import Op
# from ..op_util import OpError

# from ..opdef_util import opdef_to_opspec
# from ..opdef_util import opdef_for_opspec

# from .. import cli
# from .. import config
# from .. import op_util as oplib

# ###################################################################
# # State
# ###################################################################


# class State:
#     def __init__(self, args: Any):
#         self.args = args
#         self.restart_run = None
#         self.proto_run = None
#         self.user_op: Optional[Op] = None
#         self.batch_op: Optional[Op] = None


# ###################################################################
# # Init state
# ###################################################################


# def _init_state(args: Any):
#     S = State(args)
#     _init_user_op(S)
#     return S


# def _init_user_op(S: State):
#     assert not S.user_op, S.user_op
#     S.user_op = op = Op()
#     _init_opdef(S.args.opspec, S.args, op)


# def _init_opdef(opspec: Optional[str], args: Any, op: Op):
#     try:
#         opdef = opdef_for_opspec(opspec)
#     except OpDefNotFound:
#         raise SystemExit(
#             f"no such operation {opspec}\n"
#             "Try 'gage operations' for a list of operations."  # \
#         )
#     else:
#         op.opdef = opdef


# ###################################################################
# # Dispatch
# ###################################################################


# def _dispatch_cmd(S: State):
#     if S.args.help_op:
#         _print_op_help(S)
#     elif S.args.test_opdef:
#         _test_opdef(S)
#     elif S.args.test_sourcecode:
#         _test_sourcecode(S)
#     elif S.args.test_output:
#         _test_output(S)
#     elif S.args.test_prompt:
#         _test_prompt(S)
#     else:
#         _confirm_run(S)


# ###################################################################
# # Op help
# ###################################################################


# def _print_op_help(S: State):
#     pass


# ###################################################################
# # Test commands
# ###################################################################


# def _test_opdef(S: State):
#     assert S.user_op and S.user_op.opdef
#     opdef = S.user_op.opdef
#     print(
#         f"TODO: show how def for {opdef.name} is generated "
#         "(tbh not sure what this means)"
#     )


# def _test_sourcecode(S: State):
#     assert S.user_op and S.user_op.opdef
#     opdef = S.user_op.opdef
#     print(f"TODO: show source code copy for {opdef.name}")


# def _test_output(S: State):
#     assert S.user_op and S.user_op.opdef
#     opdef = S.user_op.opdef
#     print(f"TODO: how output is handed for {opdef.name}")


# def _test_prompt(S: State):
#     print(_prompt(S))


# ###################################################################
# # Run
# ###################################################################


# def _confirm_run(S: State):
#     if S.args.yes or _confirm(S):
#         _run(S)


# def _run(S: State):
#     assert S.user_op
#     if S.args.stage:
#         _stage_op(S.user_op, S.args)
#     else:
#         _run_op(S.user_op, S.args)


# def _stage_op(op: Op, args: Any):
#     print("TODO run")


# def _run_op(op: Op, args: Any):
#     run = oplib.init_run(op)
#     p = oplib.start_run(run, op)
#     oplib.wait_run_proc(p, run, op)


# def _handle_op_error(e: OpError):
#     print(e)
#     raise SystemExit()


# ###################################################################
# # Confirm
# ###################################################################


# def _confirm(S: State):
#     assert False, "TODO"
#     return cli.confirm(_prompt(S), default=True)


# def _prompt(S: State):
#     action = _preview_action(S)
#     subject = _preview_subject(S)
#     batch_suffix = _preview_batch_suffix(S)
#     flags_note = _preview_flags_note(S)
#     user_flags = _preview_user_flags(S)
#     optimizer_flags = _preview_optimizer_flags(S)
#     return (
#         f"You are about to {action} {subject}"
#         f"{batch_suffix}{flags_note}\n"
#         f"{user_flags}"
#         f"{optimizer_flags}"
#         "Continue?"
#     )


# def _preview_action(S: State):
#     if S.args.stage:
#         return "stage"
#     # if S.args.stage_trials:
#     #     return "stage trials for"
#     # if S.args.restart:
#     #     return "start"
#     return "run"


# def _preview_subject(S: State):
#     assert S.user_op
#     assert S.user_op.opdef
#     opspec = opdef_to_opspec(S.user_op.opdef, config.cwd())
#     # if S.restart_run:
#     #     return f"{S.restart_run.id} ({op_desc})"
#     return opspec


# def _preview_batch_suffix(S: State):
#     return ""
#     # if not S.batch_op:
#     #     return ""
#     # return "".join(
#     #     [
#     #         _batch_desc_preview_part(S.batch_op),
#     #         _batch_qualifier_preview_part(S),
#     #     ]
#     # )


# # def _batch_desc_preview_part(op):
# #     opt_name = op.opref.to_opspec(config.cwd())
# #     if opt_name == "+":
# #         return " as a batch"
# #     if opt_name in ("random", "skopt:random"):
# #         return " with random search"
# #     return f" with {opt_name} optimizer"


# # def _batch_qualifier_preview_part(S):
# #     batch_op = S.batch_op
# #     parts = []
# #     if batch_op.opref.op_name == "+":
# #         parts.append(_preview_trials_count(S))
# #     elif batch_op._max_trials:
# #         parts.append(f"{batch_op._max_trials} trials")
# #     if _is_likely_optimizer(batch_op) and batch_op._objective:
# #         parts.append(_objective_preview_part(batch_op._objective))
# #     if not parts:
# #         return ""
# #     return f" ({', '.join(parts)})"


# # def _preview_trials_count(S):
# #     trials_count = _trials_count(S)
# #     if trials_count == 1:
# #         return "1 trial"
# #     return f"{trials_count} trials"


# # def _trials_count(S):
# #     count = len(_op_trials(S.user_op))
# #     if S.batch_op._max_trials is not None:
# #         count = min(count, S.batch_op._max_trials)
# #     return count


# # def _op_trials(op):
# #     if op._batch_trials:
# #         return batch_util.expand_trial_flags(
# #             op._batch_trials,
# #             op._op_flag_vals,
# #             op._user_flag_vals,
# #             op._random_seed,
# #         )
# #     return batch_util.expand_flags(op._op_flag_vals, op._random_seed)


# # def _is_likely_optimizer(op):
# #     """Return True if op is likely an optimizer.

# #     All operations are considered likely except those known to NOT be
# #     optimizers. These are '+' (the general batch op) and 'random'.

# #     Ideally the operation would indicate if it is an optimizer but
# #     Guild doesn't support an interface for this.
# #     """
# #     return op.opref.op_name not in ("+", "random")


# # def _objective_preview_part(obj):
# #     if obj[:1] == "-":
# #         return f"maximize {obj[1:]}"
# #     return f"minimize {obj}"


# def _preview_flags_note(S: State):
#     # if S.user_op._op_flag_vals and S.user_op._batch_trials:
#     #     return " (flags below used unless specified in batch trial)"
#     return ""


# def _preview_user_flags(S: State):
#     return ""
#     # return _preview_flags(S.user_op._op_flag_vals, S.user_op._flag_null_labels)


# # def _preview_flags(flag_vals, null_labels):
# #     if not flag_vals:
# #         return ""
# #     return (
# #         "\n".join(
# #             [
# #                 f"  {_format_flag(name, val, null_labels)}"
# #                 for name, val in sorted(flag_vals.items())
# #             ]
# #         ) + "\n"
# #     )


# # def _format_flag(name, val, null_labels):
# #     if val is None:
# #         formatted = _null_label(name, null_labels)
# #     else:
# #         formatted = util.find_apply(
# #             [_try_format_function, flag_util.encode_flag_val], val
# #         )
# #     return f"{name}: {formatted}"


# # def _try_format_function(val):
# #     if not isinstance(val, str):
# #         return None
# #     try:
# #         flag_util.decode_flag_function(val)
# #     except ValueError:
# #         return None
# #     else:
# #         return val


# # def _null_label(name, null_labels):
# #     null_label = null_labels.get(name, "default")
# #     return flag_util.encode_flag_val(null_label)


# def _preview_optimizer_flags(S: State):
#     return ""
#     # if not S.batch_op or not S.batch_op._op_flag_vals:
#     #     return ""
#     # flags_preview = _preview_flags(
#     #     S.batch_op._op_flag_vals, S.batch_op._flag_null_labels
#     # )
#     # preview = f"Optimizer flags:\n{flags_preview}"
#     # return cli.style(preview, dim=True)


# ###################################################################
# # Module API
# ###################################################################


# def main(args: Any):
#     S = _init_state(args)
#     _dispatch_cmd(S)

def run(opspec: str):
    print(f"TODO: run %s")
