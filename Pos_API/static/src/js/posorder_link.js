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
 
});
