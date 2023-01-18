// odoo.define('Pos_API.PaymentScreen', function (require) {
//     const Registries = require('point_of_sale.Registries');
//     const PaymentScreen = require('point_of_sale.PaymentScreen');

//     const NewPaymentScreen = PaymentScreen =>
//      class extends PaymentScreen {
//      	constructor(){
//      		super(...arguments);
//      	}
//      	async validateOrder(isForceValidate){
//      		const order = this.currentOrder;
//      		const result = await this.env.services.rpc({model:'pos.order', method:'get_links', args:[[]]})
//      	}
//      }
//      Registries.Component.extend(PaymentScreen, NewPaymentScreen);
//      return PaymentScreen;
// });
