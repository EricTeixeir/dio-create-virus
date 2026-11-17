# Simulação de Malwares em Python — Ransomware & Keylogger

Projeto desenvolvido como parte do desafio **"Simulando um Malware de Captura de Dados Simples em Python e Aprendendo a se Proteger"**. O objetivo é **estritamente educacional**: entender, na prática, como ransomware e keylogger funcionam por dentro, para aprender a detectá-los, mitigá-los e se defender deles.

Todo o código foi escrito à mão, testado em ambiente controlado e documentado com reflexões reais sobre segurança da informação.

> **Aviso:** os scripts deste repositório não devem ser executados fora de um ambiente de testes isolado (VM, sandbox ou pasta dedicada). Eles não possuem nenhuma proteção contra uso indevido e foram criados apenas para fins de estudo.

---

## Ransomware Simulado

### O que o script faz
1. **Geração de chave** (`Fernet.generate_key()`), salva em `chave.key`.
2. **Varredura do diretório atual** (`os.getcwd()`), de forma recursiva, ignorando os próprios scripts e arquivos de controle.
3. **Criptografia simétrica** de cada arquivo encontrado, usando a biblioteca `cryptography` (Fernet).
4. **Geração da nota de resgate**, escrita em `readme.txt`, simulando a cobrança em Bitcoin (endereço fictício, apenas para fins de demonstração).
5. O script de **descriptografia** (`descrypt.py`) reverte o processo e, ao final, **apaga a chave** do disco.

### Limitações propositais (e por quê)
- **A chave ficou salva localmente**, no mesmo diretório atacado. Isso foi uma decisão consciente para facilitar o teste e garantir que os arquivos sempre pudessem ser recuperados. Em um ataque real, a chave normalmente é enviada para um servidor controlado pelo atacante (C2) e removida da máquina da vítima — é exatamente essa exfiltração que torna o ataque irreversível sem pagamento. Deixar a chave local foi o que tornou esse experimento seguro de se repetir.
- **O escopo da criptografia é o diretório de trabalho atual**, o que significa que o script foi executado **diretamente na pasta do projeto**, não em uma pasta de teste separada. Esse ponto reforça, na prática, o quão perigoso é rodar esse tipo de código fora de um ambiente isolado: um erro de diretório (`cwd` errado) seria o suficiente para atingir arquivos reais.

---

## Keylogger Simulado

### O que o script faz
- Usa a biblioteca **`pynput`** para capturar eventos de teclado globalmente.
- Grava cada tecla pressionada em `keylog.txt`, tratando teclas especiais (espaço, enter, tab, backspace, esc) e ignorando modificadores (shift, ctrl, alt, caps lock, cmd).
- A versão **`.pyw`** é a camada de "furtividade" implementada: ao rodar com essa extensão no Windows, o script é executado sem abrir uma janela de console visível, tornando-o menos perceptível para quem está usando a máquina.

### O que foi estudado, mas não implementado
- **Persistência** (rodar automaticamente na inicialização do sistema, via pasta de startup, registro do Windows ou tarefa agendada) e **técnicas de disfarce de processo** (nome genérico, mascaramento na lista de processos) foram estudadas como próximo passo lógico de um atacante real, mas não foram codificadas neste projeto. Documentar isso teoricamente já cumpre o objetivo de entender o funcionamento sem ampliar o escopo ofensivo do script.
- **Envio automático por e-mail** (via `smtplib`) **não foi implementado**. A decisão foi não configurar uma credencial/chave de e-mail real nem uma variável de ambiente só para esse teste. Vale registrar, de forma breve, que essa etapa é também a mais "visível" do ponto de vista defensivo: um keylogger local só fica perigoso quando exfiltra os dados, e é justamente a conexão de rede de saída (SMTP não autorizado) que firewalls e soluções de EDR mais facilmente detectam e bloqueiam.

---

## Reflexão sobre Defesa e Prevenção

### Antivírus
Os testes foram realizados com o **antivírus desligado** propositalmente, para permitir que o comportamento do script fosse observado sem interferência.

### Firewall
Como a etapa de envio por e-mail não foi implementada, não houve tráfego de rede de saída gerado pelos scripts. Ainda assim, é um ponto importante para a reflexão: é justamente essa comunicação de saída (keylogger enviando dados por SMTP, ou ransomware avisando um servidor C2) que um firewall bem configurado — ou uma regra de bloqueio de saída não autorizada — teria a chance de identificar e barrar antes da exfiltração dos dados.

### Sandboxing
Os testes foram realizados dentro de uma **máquina virtual com Kali Linux**, isolada do sistema principal. Essa escolha evitou qualquer risco de os scripts afetarem arquivos reais fora do ambiente de teste, mesmo com o ransomware atuando sobre o diretório de trabalho atual. Esse é um dos principais motivos pelos quais análises de malware (mesmo simuladas) devem sempre ocorrer em ambientes isolados e descartáveis.

### Conscientização do usuário
Na prática, tanto o ransomware quanto o keylogger dependem de um primeiro passo humano: a execução do arquivo. Nenhum dos dois scripts se auto-propaga ou explora uma vulnerabilidade de sistema — eles dependem inteiramente de alguém clicar, baixar ou rodar o arquivo errado. Isso evidencia por que treinamento e conscientização sobre phishing, downloads de fontes não confiáveis e engenharia social continuam sendo uma das defesas mais eficazes (e mais baratas) contra esse tipo de ameaça.

---

## Aprendizados

- A parte **técnica** de criar um ransomware ou keylogger básico é surpreendentemente simples — bibliotecas como `cryptography` e `pynput` tornam a barreira de entrada baixa.
- A parte **difícil de verdade** é a defesa: detectar comportamento anômalo, controlar tráfego de saída e, principalmente, reduzir a chance de execução inicial (conscientização do usuário).
- Rodar esse tipo de experimento em **ambiente isolado (VM)** não é opcional — é o que torna o aprendizado seguro.
- Entender a lógica do ataque (mesmo em uma versão simplificada) ajuda a entender exatamente onde e como aplicar as camadas de defesa.

---

## Como executar (apenas em ambiente controlado)

```bash
pip install cryptography pynput

# Ransomware
python Ransomware/Ransomware.py     # criptografa os arquivos de teste
python Ransomware/descrypt.py       # reverte a criptografia

# Keylogger
python Keylogger/keylogger.py       # versão com console
# ou
python Keylogger/keylogger.pyw      # versão sem console (Windows)
```

