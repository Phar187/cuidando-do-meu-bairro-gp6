import { mount, createLocalVue } from '@vue/test-utils';
import Vuex from 'vuex';
import MsgShower from '@/components/MsgShower.vue';

const localVue = createLocalVue();
localVue.use(Vuex);

localVue.mixin({
  methods: {
	$t: (msg) => msg
  }
});

describe('MsgShower.vue', () => {
  let state;
  let mutations;
  let store;

  beforeEach(() => {
	state = {
  	msgs: {
    	msgs: [
      	{ id: 1, text: 'Mensagem 1' },
      	{ id: 2, text: 'Mensagem 2' }
    	]
  	}
	};

	mutations = {
  	removeMsg: jest.fn()
	};

	store = new Vuex.Store({
  	state,
  	mutations
	});
  });

  it('renderiza a mensagem', () => {
	const wrapper = mount(MsgShower, { store, localVue });
	const messages = wrapper.findAll('#toast-bottom-right');

	expect(messages.length).toBe(2);
	expect(messages.at(0).text()).toContain('Mensagem 1');
  });

  it('remove a mensagem ao clicar no botão de fechar', async () => {
	const wrapper = mount(MsgShower, { store, localVue });
	const closeButton = wrapper.findAll('button').at(0);

	await closeButton.trigger('click');

	expect(mutations.removeMsg).toHaveBeenCalled();
  });

  it('não exibe mensagens se o array msgs estiver vazio', () => {
	// Define o estado msgs vazio
	state.msgs.msgs = [];
	const wrapper = mount(MsgShower, { store, localVue });
	const messages = wrapper.findAll('#toast-bottom-right');

	expect(messages.length).toBe(0);
  });

  it('renderiza corretamente quando há várias mensagens', () => {
	// Define várias mensagens no estado
	state.msgs.msgs = [
  	{ id: 1, text: 'Mensagem 1' },
  	{ id: 2, text: 'Mensagem 2' },
  	{ id: 3, text: 'Mensagem 3' }
	];
	const wrapper = mount(MsgShower, { store, localVue });
	const messages = wrapper.findAll('#toast-bottom-right');

	expect(messages.length).toBe(3);
	expect(messages.at(0).text()).toContain('Mensagem 1');
	expect(messages.at(1).text()).toContain('Mensagem 2');
	expect(messages.at(2).text()).toContain('Mensagem 3');
  });

});


