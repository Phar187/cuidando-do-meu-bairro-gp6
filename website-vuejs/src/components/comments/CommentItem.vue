<template>
  <div class="comment-item border-b border-gray-200">
      <div>
          <div class="flex items-center space-x-4">
            <div class="flex-shrink-0">
              <img class="icon" :src="$assets.aComTop">
            </div>
            <div class="flex-1 min-w-0">
                <p class="text-base font-medium text-neutral-base truncate" v-if="!comment.hidden && !isEditting">
                {{ comment.text }}
                </p>
                <p v-if="comment.hidden" class="text-sm font-medium text-neutral-base truncate">
                  {{ $t('Comment removed.') }}
                </p>
                <p class="text-sm text-neutral-light truncate">
                  <router-link :to="{ name: 'pessoa', params: { viewingUser: comment.author} }">
                      {{ comment.author }}
                  </router-link>
                </p>
            </div>
            <div class="inline-flex items-baseline text-base font-semibold text-neutral-base">
                <span class="mr-2">{{ formatDate(comment.created) }}</span>
              <br>
              <span class="text-xs text-neutral-light" v-if="comment.created.getTime() !== comment.modified.getTime()">
                Modificado ({{ formatDate(comment.modified) }})
              </span>
              <!-- <span>+{{comment.upvotes}}/-{{comment.downvotes}}</span> -->
            </div>
            <div>
              <button 
              class="hidden sm:inline-block text-gray-500 hover:bg-gray-100 rounded-lg text-sm p-1.5" type="button"
              v-click-outside="closeListComment"
              @click="toggleListComment">
                <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z"></path></svg>
              </button>
              <!-- Dropdown menu -->
              <div v-if="openCommentList" class="absolute z-10 w-20 -ml-10 text-base list-none bg-white rounded divide-y divide-gray-100 shadow">
                  <ul class="py-1">
                    <li>
                      <a v-if="!isEditting"
                          class="cursor-pointer block py-2 px-4 text-sm text-gray-700 hover:bg-gray-100"
                          @click="isEditting = true">
                        {{ $t("edit") }}
                      </a>
                    </li>
                    <li>
                      <button-spinner
                        @click.prevent.native="sendDelete({ url: comment.url, id: comment.id })"
                        :condition="pending.delete[comment.id]"
                        class="cursor-pointer block py-2 px-4 text-sm text-gray-700 hover:bg-gray-100">
                          {{ $t("Delete") }}
                      </button-spinner>
                    </li>
                  </ul>
              </div>
            </div>
          </div>
          <div class="flex items-center space-x-4 py-3">
           <div class="inline-flex items-center">
              <!-- Control buttons -->
              <button class=" text-secondary-base ml-10 underline"
                v-if="!isEditting"
                @click="isReplying = true"
                @focus="requireLogin">
                {{ $t("reply") }}
              </button>
              <!-- Not Author buttons -->
                <div v-if="!isAuthor" class="bullet mx-2 text-secondary-base">•</div>
                <button-spinner
                  v-if="!isAuthor"
                  class="text-secondary-base"
                  @focus.native="requireLogin"
                  :condition="pending.voteup[comment.id]"
                  @click.prevent.native="sendVote({ url: comment.vote_url, id: comment.id, vote: true })">
                    Curtir {{ pending.voteup.length }}
                </button-spinner>
                <div v-if="!isAuthor" class="bullet mx-2 text-secondary-base">•</div>
                <button-spinner
                  v-if="!isAuthor"
                  class=" text-secondary-base "
                  @focus.native="requireLogin"
                  :condition="pending.votedown[comment.id]"
                  @click.prevent.native="sendVote({ url: comment.vote_url, id: comment.id, vote: false })">
                    Descurtir
                </button-spinner>
                <div v-if="!isAuthor" class="bullet mx-2 text-secondary-base">•</div>
                <button-spinner
                  class=" text-secondary-base "
                  v-if="!comment.hidden && !isAuthor "
                  :title="$t('Report comment as inappropriate')"
                  :condition="pending.report[comment.id]"
                  @click.prevent.native="sendReport({ url: comment.report_url, id: comment.id })">
                    {{ $t('Report') }}
                </button-spinner>
            </div>
          </div>
          <!-- Icon for replies to top most comments -->
          <div v-if="!top" class="comment-icon not-comment-top">
            <img class="icon w-5" :src="$assets.aCom">
          </div>

          <div class="comment-flex">
              <div class="comment-text">

                  <!-- Edit form -->
                  <form class="form" v-if="isEditting">
                      <div class="form-group">
                          <label class="sr-only"
                                  :for="`comment-edit-textarea-${comment.id}`">
                              {{ $t('Edit comment') }}
                          </label>
                          <textarea
                            :id="`comment-edit-textarea-${comment.id}`"
                            class="form-control bg-gray-50 border border-gray-300 text-neutral-base text-sm rounded-lg focus:ring-primary-dark focus:border-primary-dark block w-full p-2.5" 
                            maxlength="500"
                            v-model="edit"
                            rows="3"/>
                      </div>
                      <button-spinner
                        type="submit"
                        @click.prevent.native="sendEditAndClose"
                        :condition="pending.edit[comment.id]"
                        class="my-5 text-white cursor-pointer bg-secondary-light hover:bg-secondary-base focus:ring-4 focus:outline-none font-medium rounded-lg text-sm px-4 py-2 text-center">
                          {{ $t('Save') }}
                      </button-spinner>
                      <a v-if="isEditting"
                          class="my-5 text-secondary-light cursor-pointer border border-secondary-light hover:bg-secondary-light hover:text-white font-medium rounded-lg text-sm px-4 py-2 text-center"
                          @click="isEditting = false">
                        {{ $t("Cancel") }}
                      </a>
                  </form>

                  
              </div>
          </div>

          
        <div>
            <!-- Reply form -->
            <form class="form" v-if="isReplying">
                <div class="form-group">
                    <label class="sr-only"
                           for="comment-reply-textarea-{comment.id}">
                        {{ $t('Reply Comment') }}
                    </label>
                    <textarea
                      id="comment-reply-textarea-{comment.id}"
                      class="form-control bg-gray-50 border border-gray-300 text-neutral-base text-sm rounded-lg focus:ring-primary-dark focus:border-primary-dark block w-full p-2.5" 
                      maxlength="500"
                      v-model="reply"
                      rows="3"/>
                </div>
                <button-spinner type="submit"
                        @click.prevent.native="_sendReply({ url: comment.url, text: reply, id: comment.id })"
                        :condition="pending.reply[comment.id]"
                        :disabled="!reply.length"
                        class="my-5 text-white cursor-pointer bg-secondary-light hover:bg-secondary-base focus:ring-4 focus:outline-none font-medium rounded-lg text-sm px-4 py-2 text-center">
                    {{ $t('Send') }}
                </button-spinner>
                <button  class="my-5 text-secondary-light cursor-pointer border border-secondary-light hover:bg-secondary-light hover:text-white font-medium rounded-lg text-sm px-4 py-2 text-center"
 @click.prevent.native="isReplying = false">
                    {{ $t('Cancel') }}
                </button>
            </form>
        </div>
      </div>
      <!-- Replies list -->
      <comment-item v-for="(reply, i) in comment.replies" :key="i" style="margin: 20px;" :comment="reply"/>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'
import { formatDate } from '@/utils'
export default {
  name: 'comment-item',
  props: {
    comment: Object,
    top: {
      type: Boolean,
      default: false
    }
  },
  data () {
    return {
      isEditting: false,
      isReplying: false,
      edit: this.comment.text,
      reply: '',
      openCommentList: false
    }
  },
  computed: {
    isAuthor () {
      return this.comment.author === this.username
    },
    ...mapState({
      username: state => state.auth.username,
      pending: state => state.comments.pending
    })
  },
  methods: {
    formatDate,
    async sendEditAndClose () {
      await this.sendEdit({ url: this.comment.url, text: this.edit, id: this.comment.id })
      this.isEditting = false
    },
    _sendReply (data) {
      this.sendReply(data)
      // TODO: só remover o texto e fechar caixa se não der erro
      this.isReplying = false
      this.reply = ''
    },
    toggleListComment () {
      this.openCommentList = !this.openCommentList
    },
    closeListComment () {
      this.openCommentList = false
    },
    ...mapActions([
      'requireLogin',
      'sendDelete',
      'sendVote',
      'sendEdit',
      'sendReport',
      'sendReply'
    ])
  }
}
</script>
