<template>
    <div v-if="Object.keys(subscriptions).length && viewingUser === username">
    <div class="w-full bg-white rounded-lg border border-gray-200 shadow-md p-5">
      <h2 class="text-neutral-base text-2xl font-bold mb-5">Itens Acompanhados</h2>
      <li class="flex justify-between items-center p-5 border-b border-gray-200 text-neutral-base" v-for="subscription in subscriptions" :key="subscription.tag">
        <a class="underline text-neutral-base" :href="subscription.template_data.link">
          {{ subscription.tag }}
        </a>
        <button-spinner
          type="submit" @click.prevent.native="unsubscribe({ tag: subscription.tag })"
          :condition="pending.unsubscribe[subscription.tag]"
          class="self-center py-2 px-4 text-sm font-medium text-center text-white bg-secondary-light rounded-lg hover:bg-secondary-base"
        >
          {{ $t("Unfollow") }}
        </button-spinner>
      </li>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'
export default {
  name: 'user-subscriptions',
  computed: {
    ...mapState({
      subscriptions: state => state.subscriptions.subscriptions,
      pending: state => state.subscriptions.pending,
      viewingUser: state => state.route.params.viewingUser,
      username: state => state.auth.username
    })
  },
  methods: {
    ...mapActions(['unsubscribe'])
  }
}
</script>
