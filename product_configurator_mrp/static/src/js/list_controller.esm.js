import {ListController} from "@web/views/list/list_controller";
import {applyConfigButtonMixin} from "./config_button_mixin.esm.js";
import {patch} from "@web/core/utils/patch";

patch(ListController.prototype, {});
applyConfigButtonMixin(ListController.prototype, ".o_list_button_add_config");
