import {FormController} from "@web/views/form/form_controller";
import {applyConfigButtonMixin} from "./config_button_mixin.esm.js";
import {patch} from "@web/core/utils/patch";

patch(FormController.prototype, {});
applyConfigButtonMixin(FormController.prototype, ".o_form_button_create_config");
