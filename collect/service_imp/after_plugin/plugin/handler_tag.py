from collect.service_imp.after_plugin.after_plugin import AfterPlugin
from collect.utils.collect_utils import get_safe_data


class HandlerTag(AfterPlugin):
    HTConst = {
        "result_tag_name": "result_tag"
    }

    def get_result_tag_name(self):
        return self.HTConst["result_tag_name"]

    def handler(self, result, template):
        params_result = self.get_params_result(template)
        result_tag = get_safe_data(self.get_result_tag_name(), template)
        other = {}
        for key in result_tag:
            if key in params_result:
                other[key] = params_result[key]
        return self.success(result, other=other)
