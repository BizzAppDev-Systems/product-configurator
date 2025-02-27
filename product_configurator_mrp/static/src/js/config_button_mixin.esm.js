const {document} = globalThis;
import {onMounted} from "@odoo/owl";
import {useService} from "@web/core/utils/hooks";

export function applyConfigButtonMixin(controllerProto, buttonSelector) {
    const originalSetup = controllerProto.setup;
    controllerProto.setup = function (...args) {
        if (originalSetup) {
            originalSetup.apply(this, args);
        }
        this.orm = useService("orm");
        this.actionService = useService("action");

        onMounted(() => {
            const rootEl = this.el || document;
            const button = rootEl.querySelector(buttonSelector);
            if (button && this.props && this.props.resModel === "mrp.production") {
                button.style.display = "block";
            }
        });
    };

    controllerProto._onConfigure = async function () {
        const action = await this.orm.call(
            "mrp.production",
            "action_config_start",
            [],
            {}
        );
        if (action) {
            this.actionService.doAction(action);
        }
    };
}
