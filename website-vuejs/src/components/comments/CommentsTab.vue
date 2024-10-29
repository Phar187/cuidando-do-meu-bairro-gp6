<template>
  <div>
    <h3 class="text-neutral-base font-semibold text-xl">{{ $t('See the comments about this expense') }}</h3>

    <form class="form mt-3">
      <div v-if="!username">
        <button class="btn btn-color-sec relative text-right text-white px-3 py-2 cursor-pointer bg-secondary-light font-light hover:bg-secondary-base rounded" @click="requireLogin">Faça login</button>
      </div>
      <div v-else>
        <div class="form-group">
          <label class="sr-only" for="comment-textarea">
              {{ $t('Comment') }}
          </label>
          <textarea
              id="comment-textarea"
              rows="3"
              maxlength="500"
              class="form-control bg-gray-50 border border-gray-300 text-neutral-base text-sm rounded-lg focus:ring-primary-dark focus:border-primary-dark block w-full p-2.5" 
              v-model="text"
              :placeholder="$t('Your comment')"/>
        </div>
        <button-spinner type="submit"
          @click.prevent.native="_sendComment({ key: page.name, text })"
          :disabled="!text.length"
          :condition="pending.reply[page.name]"
          class="mt-5 text-white cursor-pointer bg-secondary-light hover:bg-secondary-base focus:ring-4 focus:outline-none font-medium rounded-lg text-sm px-5 py-2.5 text-center"
        >
          {{ $t("Send comment") }}
        </button-spinner>
      </div>
    </form>

    <div class="comments-block my-10 w-full">
      <comment-item v-for="(comment, i) in page.comments"
                    :key="i" :top="true" :comment="comment"/>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'
import CommentItem from '@/components/comments/CommentItem.vue'

export default {
  name: 'comments-tab',
  components: {
    CommentItem
  },
  data () {
    return {
      text: ''
    }
  },
  computed: mapState({
    page: state => state.comments.commentsPage,
    pending: state => state.comments.pending,
    username: state => state.auth.username,
  }),
  methods: {
    async _sendComment (data) {
      await this.sendComment(data)
      // TODO: só remover o texto se não der erro
      this.text = ''
    },
    ...mapActions(['sendComment', 'requireLogin'])
  }
}
</script>
