import config from 'config'
import ajax from '../utils/ajax.js'
import MapStore from './mapStore'
import auth from './auth'
import msgs from '../store/msgs'
import {registerSignals} from '../utils/helpers'

var api = config.apiurl_subscriptions


class Subscriptions extends MapStore {
    constructor(signal) {
        super(signal)
        this.forceKey = 's'
        registerSignals(
            this,
            'subscribe unsubscribe',
            true
        )
    }
    ajaxParams(key) {
      // TODO: Não enviar se user for none
      return {
        url: `${api}/subscriptions`,
        method: 'post',
        data: {
            subscriber: auth.getUsername()
        }}
    }
    processResponse(json) {
        // orderComments(json.comments)
      let subscriptions = {}
      json.subscriptions.forEach((s) => subscriptions[s.tag] = s)
        return subscriptions
    }

    async _subscribe(tag, author, errorMsg) {
      let params = {
        url: `${api}/subscriptions`,
        method: 'put',
        data: {
          token: await auth.getMicroToken(),
          subscriptions: [{
            tag,
            author,
            template_data: {link: window.location.href}
          }]}}

        let json = null
        try {
            json = await ajax(params)
            if (json) {
              this.load('eusinho', true)
            }
        } catch(err) {
            msgs.addError(errorMsg)
        }
        return json
    }

    // Subscribe
    async subscribe(params) {
      return await this._subscribe(params.id, params.author, 'Error to subscribe')
    }

  // Unsubscribe
  async unsubscribe(params) {
    return await this._unsubscribe(params.id, 'Error to subscribe')
  }

  // // Subscribe to pedido
  // async subscribePedido(params) {
  //   return await this.subscribe(params.id, params.author, 'Error to subscribe')
  // }

  async _unsubscribe(tag, errorMsg) {
    let params = {
      url: `${api}/subscriptions`,
      method: 'delete',
      data: {
        token: await auth.getMicroToken(),
        tags: [tag]}}

    let json = null
    try {
      json = await ajax(params)
      if (json) {
        this.load('eusinho', true)
      }
    } catch(err) {
      msgs.addError(errorMsg)
    }
    return json
  }

}

let subscriptions = new Subscriptions('subscriptions')

export default subscriptions
