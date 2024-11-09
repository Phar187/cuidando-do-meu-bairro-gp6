# language: pt
Funcionalidade: Visualização e Acompanhamento de Gastos por Instituição

Contexto:
    Dado que estou na página inicial

    #Cenário 1: Verificar os gastos planejados, empenhados e liquidados de uma determinada despesa pela tabela. O usuário tem certeza que tal despesa existe.
    Cenário: Verificação de gastos existentes
        Então eu clico em "Administração da Unidade" na tabela de distribuição de recursos
        E eu deveria ver as despesas de "Administração da Unidade"
        
    #Cenário 2: Verificar os gastos planejados, empenhados e liquidados de uma determinada despesa que não está na tabela.
    Cenário: Verificação de gastos inexistentes
        Então eu procuro "String aleatória" na tabela de distribuição de recursos
        E eu não deveria encontrar "String Aleatória"
