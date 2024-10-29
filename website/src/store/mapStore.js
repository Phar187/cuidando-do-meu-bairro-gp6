import ajax from '../utils/ajax.js'
import {sleep} from '../utils/helpers.js'
import msgs from './msgs'

export default class MapStore {
    constructor(signal) {
        this.init(signal)
    }

    // These need to be defined
    // ajaxParams(key) { return params }
    processResponse(json) { return json }

    init(signal) {
        riot.observable(this)

        this._map = {}

        this.signal = signal

        this.on(riot.VEL(this.signal), (key, force) => {
            // console.log('mapstore:signal', this.signal, 'key:', key)
            if (this.forceKey) key = this.forceKey
            if (key) this.load(key, force)
        })
        riot.control.addStore(this)
    }

    async load(key, force) {
        // If doesn't have current key data, load
        let current = this._map[key]
        if (current === undefined || force) {
            this._map[key] = 'loading'

            let keep_trying = 5
            while (keep_trying) {
                try {
                    let json = await ajax(await this.ajaxParams(key))
                    if (json) {
                        this._map[key] = await this.processResponse(json)
                        keep_trying = 0
                    } else {
                        return null
                    }
                } catch(err) {
                    keep_trying--
                    if (!keep_trying) {
                        msgs.addError('error_mapstore_ajax')
                        return null
                    }
                    // sleeps 500, 1000, 2000 and 4000 ms
                    await sleep(8000/Math.pow(2, keep_trying))
                }
            }
        }
        this.triggerChanged(key)
        return null
    }

    triggerChanged(key) {
        let value = this._map[key]
        if (value == 'loading') value = undefined
        this.trigger(riot.SEC(this.signal), {key, value})
    }
}
