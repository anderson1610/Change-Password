# Change-Password
Feito para uso corporativo, na empresa na qual trabalho temos muita demanda de acessar as maquina remotas e realizar a troca de senha de determinado perfil, com esse script podemos acessar o cmd, com o psexec, economizando tempo de trabalho.

Necessario ter conhecimentos basicos de psexec.
Range de IP muda de acordo com a rede que será utilizado, basta mudar manualmente na linha 26, variavel 'comando'.
Para funcionar, a maquina na qual irá rodar o script precisa estar logado em um usuario administrador, que possui nome e senha iguais ao usuario administrador das demais maquinas que será realizada a troca de senha.
Nome de usuarios, que será mudado a senha, muda conforme sua necessidade, basta mudar manualmente na linha 87.
