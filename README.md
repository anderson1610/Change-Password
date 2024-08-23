# Change-Password
Este script foi desenvolvido para uso corporativo na empresa onde trabalho, onde há uma grande demanda para acessar máquinas remotas e realizar a troca de senha de determinados perfis. Com este script, podemos acessar o CMD usando o PsExec, economizando tempo de trabalho.

É necessário ter conhecimentos básicos de PsExec. O intervalo de IP muda de acordo com a rede utilizada e pode ser ajustado manualmente na variável ‘comando’. Para que o script funcione, a máquina na qual ele será executado precisa estar logada com um usuário administrador, com nome e senha idênticos ao usuário administrador das demais máquinas onde a troca de senha será realizada. O nome dos usuários, cujas senhas serão alteradas, pode ser ajustado conforme necessário, bastando mudar manualmente.

Caso a máquina não possua o PsExec, basta extrair o arquivo compactado e colocá-lo na área de trabalho (Desktop) que o programa fará o restante.

Qualquer sugestão de melhoria é bem-vinda. Estou aberto a novos aprendizados. Obrigado!
