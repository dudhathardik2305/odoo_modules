// odoo.define('Pos_API.orderlink', function(require){
//     'use strict';
//     var models = require('point_of_sale.models');
//     var _super_product = models.PosModel.prototype;
//     models.PosModel = models.PosModel.extend({
//         initialize: function(session, attributes){
//             var self = this;
//             console.log('\n\n this one is added\n\n');
//             // models.load_fields('product.product', ['new_field']);
//             // _super_product.initialize.apply(this, arguments);
//         }
//     });
// });


odoo.define('Pos_API.orderlink', function (require) {
    'use strict';

    console.log('\n\njs file has loaded\n\n'); 
    var { PosGlobalState, Order, Orderline } = require('point_of_sale.models');
    const Registries = require('point_of_sale.Registries');


const Raju = (Order) => class Raju extends Order {
    constructor() {
        super(...arguments);
        // this.links = this.links || false;
        this.save_to_db();
    }
   
    getCustomerCount(){
        // var new_link = await this.pos.env.services.rpc({
        //     model: 'pos.order',method: 'get_links'
        // })
        return Object.keys(this.pos.validated_orders_name_server_id_map)[0];
    }

        //@override
    export_as_JSON() {
        const json = super.export_as_JSON(...arguments);
        // if (this.pos.config.module_pos_restaurant) {
            // if (this.pos.config.iface_floorplan) {
            //     json.table_id = this.tableId
            // }
        // json.links = this.links;
        // }
        // if (this.pos.config.iface_printers) {
        //     json.multiprint_resume = JSON.stringify(this.printedResume);
        //     // so that it can be stored in local storage and be used when loading the pos in the floorscreen
        //     json.printing_changes = JSON.stringify(this.printingChanges);
        // }
        return json;
    }
    //@override
    init_from_JSON(json) {
        super.init_from_JSON(...arguments);
        // this.links = json.links;

    }
    //@override
    export_for_printing() {
        const json = super.export_for_printing(...arguments);
        return _.extend(json, {'links': this.getCustomerCount()});
    }
   
}
Registries.Model.extend(Order, Raju);
 
    // const models = require('point_of_sale.models');
    // models.load_fields('res.partner', 'links');
});
