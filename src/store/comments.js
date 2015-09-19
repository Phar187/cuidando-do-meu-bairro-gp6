import config from 'config'
import ajax from '../utils/ajax.js'
import MapStore from './mapStore'
import auth from './auth'

var api = config.apiurl_comments


function commentCompare(a, b) {return a.created > b.created ? 1 : -1}

function orderComments(comments) {
    comments.sort(commentCompare)
    for (let com of comments) {
        if (com.replies) orderComments(com.replies)
    }
    return comments
}


class Comments extends MapStore {
    constructor(signal) {
        super(signal)
        // Register signals
        for (let endname of ['Comment', 'Delete', 'Report',
                             'Reply', 'Edit', 'Vote']) {
            let name = `send${endname}`
            this.on(riot.VEC(name), params => this[name](params))
        }
    }
    ajaxParams(key) {
        let url = `${api}/thread/${key}`,
            method = 'get'
        return {url, method}
    }
    processResponse(response) {
        orderComments(response.json.comments)
        return response.json
    }

    updateThread(response) {
        let key = response.json.name
        this._map[key] = this.processResponse(response)
        this.triggerChanged(key)
    }

    // Add comment to a thread
    async sendComment(params) {
        let url = `${api}/thread/${params.code}`,
            data = {
                'token': await auth.getMicroToken(),
                'text': params.text,
            }
        this.updateThread(await ajax({url, data, method: 'post'}))
            // .then(this.processResponse.bind(this))
            // .then((response) => {
            //     this._map[params.code] = response
            //     this.triggerChanged(params.code)
            // })
            // this.trigger(riot.SEC('comments'), this.username)
    }

    // Reply to a comment
    async sendReply(params) {
        let url = api + params.url,
            data = {
                'token': await auth.getMicroToken(),
                'text': params.text,
            }
        this.updateThread(await ajax({url, data, method: 'post'}))
    }

    // Edit a comment
    async sendEdit(params) {
        let url = api + params.url,
            data = {
                'token': await auth.getMicroToken(),
                'text': params.text,
            }
        this.updateThread(await ajax({url, data, method: 'put'}))
    }

    // Delete a comment
    async sendDelete(params) {
        let url = api + params.url,
            data = {
                'token': await auth.getMicroToken(),
            }
        this.updateThread(await ajax({url, data, method: 'delete'}))
    }

    // Report a comment
    async sendReport(params) {
        let url = api + params.url
            // data = {
            //     'token': await auth.getMicroToken(),
            // }
        this.updateThread(await ajax({url, method: 'post'}))
    }

    // Upvote/downvote comment from a thread
    // vote == true: upvote; vote == false: downvote
    async sendVote(params) {
        let url = api + params.url,
            data = {
                'token': await auth.getMicroToken(),
                'vote': params.vote
            }
        this.updateThread(await ajax({url, data, method: 'post'}))
    }
}

let comments = new Comments('comments')

export default comments
