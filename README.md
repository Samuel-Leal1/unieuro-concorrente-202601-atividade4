# Relatório da Aplicação de Filtro em Imagem de Forma Paralela
  
---

| Campo      | Informação                        |
|------------|-----------------------------------|
| Disciplina | Computação Paralela e Distribuída |
| Aluno      | Samuel Leal de Araujo             |
| Aluno      | Marcelo Oliveira                  |
| Aluno      | Kaio Kevin                        |
| Aluno      | William Alencar                   |
| Professor  | Rafael Marconi Ramos              |
| Data       | 27/03/2026                        |

---
## 1. Descrição do Problema 

O problema consiste na conversão de uma imagem grande no formato PPM para escala de cinza.

Como o programa fornecido não pode ser alterado, a paralelização foi realizada externamente, dividindo a imagem em partes menores e processando cada parte em paralelo com múltiplas threads.

Após o processamento, as partes são reunidas para formar a imagem final.

Objetivo: reduzir o tempo de processamento da imagem
Volume de dados: imagem de ~16 GB
Algoritmo: divisão de dados + execução paralela via threads/subprocessos
Complexidade: O(N) (número de pixels)
---
## 2. Ambiente Experimental 

| Item                        | Descrição              |
| --------------------------- | ---------------------- |
| Processador                 | Ryzen 5 3600X          |
| Número de núcleos           | 6 núcleos / 12 threads |
| Memória RAM                 | 16 GB                  |
| Sistema Operacional         | Windows 11             |
| Linguagem utilizada         | Python 3.14            |
| Biblioteca de paralelização | threading + subprocess |
| Compilador / Versão         | CPython 3.14           |

---- 
## 3. Metodologia de Testes 

O tempo foi medido com time.time(), considerando o tempo total do processamento.

Foi realizada 1 execução por configuração, sem controle de carga do sistema.

Configurações testadas
2 threads
4 threads
8 threads
12 threads

Procedimento experimental
Execução única por configuração
Sem cálculo de média
Execução em máquina local
Processamento com leitura e escrita intensiva em disco
---
## 4. Resultados Experimentais 

| Nº Threads | Tempo (s) |
| ---------- | --------- |
| 2          | 160.47    |
| 4          | 116.07    |
| 8          | 114.59    |
| 12         | 58.94     |

---
## 5. Cálculo de Speedup e Eficiência

**Speedup:**
```
Speedup(p) = T(1) / T(p)
```

Onde:
- `T(1)` = tempo da execução com 1 processo (baseline)
- `T(p)` = tempo com `p` processos

**Eficiência:**
```
Eficiência(p) = Speedup(p) / p
```

Onde:
- `p` = número de processos

---
## 6. Tabela de Resultados 

| Threads | Tempo (s) | Speedup | Eficiência |
| ------- | --------- | ------- | ---------- |
| 2       | 160.47    | 0.774   | 0.387      |
| 4       | 116.07    | 1.069   | 0.267      |
| 8       | 114.59    | 1.084   | 0.136      |
| 12      | 58.94     | 2.107   | 0.176      |

--- 
## 7. Gráfico de Tempo de Execução

<img width="485" height="295" alt="processosTempo" src="https://github.com/user-attachments/assets/659499bf-02ff-401d-82f7-9503a05445ba" />

- **Eixo X:** número de processos
- **Eixo Y:** tempo de execução (segundos)

---

## 8. Gráfico de Speedup

<img width="488" height="299" alt="threadsSpeedup" src="https://github.com/user-attachments/assets/5f1b320d-dbcf-4511-8b55-2252734dcee1" />

- **Eixo X:** número de processos
- **Eixo Y:** speedup
- Incluir linha de speedup ideal (linear) para comparação

---

## 9. Gráfico de Eficiência

<img width="487" height="296" alt="threadsEficiencia" src="https://github.com/user-attachments/assets/8c6f026b-ee0a-46cd-b3ab-9c5502886bab" />

- **Eixo X:** número de processos
- **Eixo Y:** eficiência (valores entre 0 e 1)

---

## 10. Análise dos Resultados 

Os resultados mostram que o paralelismo trouxe ganho de desempenho apenas em configurações com maior número de threads, especialmente com 12 threads.

Speedup

O speedup máximo foi 2.10x (12 threads), abaixo do ideal.

Escalabilidade

A aplicação apresentou escalabilidade parcial, com melhora significativa apenas em 12 threads.

Eficiência

A eficiência diminui conforme o número de threads aumenta.

Principais fatores
Gargalo de I/O (acesso ao disco)
Overhead de criação de subprocessos
Concorrência por CPU e disco

--- 
## 11. Conclusão 

O paralelismo trouxe ganho moderado de desempenho, reduzindo o tempo de execução de 180.34 s para 58.94 s com 12 threads.

O ganho não foi linear devido a limitações de I/O e overhead de processos.

O melhor desempenho foi obtido com 12 threads, alinhado ao hardware disponível.

Melhorias futuras
 reduzir acessos ao disco
 evitar subprocessos
 executar múltiplas vezes e calcular média
 otimizar leitura/escrita de arquivos
