from collect.service_imp.after_plugin.after_plugin import AfterPlugin
from collect.utils.collect_utils import get_safe_data


class HandlerResult(AfterPlugin):
    def handler(self, result, template):
        params_result = self.get_params_result(template)
        result_handlers = get_safe_data(self.get_result_handler_name(), template)
        # 处理结果
        msg = ""
        if result_handlers:
            for result_handler in result_handlers:
                if not self.is_enable(params_result, result_handler):
                    continue
                from collect.service_imp.result_handlers.result_handler import ResultHandler
                h = ResultHandler(op_user=self.op_user)
                if self.can_log(template):
                    config = get_safe_data(self.get_key_name(), result_handler)
                    self.log(msg="进入处理器结果" + config)
                result_data = h.handler(result, result_handler, template)
                if self.is_success(result_data):
                    result = self.get_data(result_data)
                    msg = self.get_msg(result_data)
                else:
                    return result_data
        return self.success(result, msg=msg)
