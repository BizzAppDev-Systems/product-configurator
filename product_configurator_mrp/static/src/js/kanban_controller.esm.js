import {KanbanController} from "@web/views/kanban/kanban_controller";
import {applyConfigButtonMixin} from "./config_button_mixin.esm.js";
import {patch} from "@web/core/utils/patch";

patch(KanbanController.prototype, {});
applyConfigButtonMixin(KanbanController.prototype, ".o-kanban-button-new_config");
