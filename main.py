import json
import os

class Tarefa:
    def __init__(self, titulo: str, concluida: bool = False):
        self.titulo = titulo
        self.concluida = concluida

    def marcar_como_concluida(self):
        """Altera o status da tarefa para concluída."""
        self.concluida = True

    def para_dicionario(self) -> dict:
        """Converte a tarefa em dicionário para facilitar salvar em JSON."""
        return {
            "titulo": self.titulo,
            "concluida": self.concluida
        }

    @staticmethod
    def de_dicionario(dados: dict):
        """Cria um objeto Tarefa a partir de um dicionário."""
        return Tarefa(titulo=dados["titulo"], concluida=dados["concluida"])

    def __str__(self) -> str:
        """Retorna uma representação amigável para exibição no terminal."""
        status = "[✓] Concluída" if self.concluida else "[ ] Pendente"
        return f"{status} - {self.titulo}"


class GerenciadorTarefas:
    def __init__(self, arquivo_dados: str = "tarefas.json"):
        self.arquivo_dados = arquivo_dados
        self.tarefas: list[Tarefa] = []
        self.carregar_tarefas()

    def adicionar_tarefa(self, titulo: str):
        """Cria e adiciona uma nova tarefa à lista."""
        nova_tarefa = Tarefa(titulo)
        self.tarefas.append(nova_tarefa)
        self.salvar_tarefas()
        print(f"Tarefa '{titulo}' adicionada com sucesso!")

    def listar_tarefas(self):
        """Exibe todas as tarefas no terminal com numeração."""
        if not self.tarefas:
            print("\nNenhuma tarefa cadastrada.")
            return

        print("\n--- LISTA DE TAREFAS ---")
        for idx, tarefa in enumerate(self.tarefas, start=1):
            print(f"{idx}. {tarefa}")
        print("------------------------")

    def concluir_tarefa(self, indice: int):
        """Marca a tarefa correspondente ao número/índice como concluída."""
        if 1 <= indice <= len(self.tarefas):
            tarefa = self.tarefas[indice - 1]
            tarefa.marcar_como_concluida()
            self.salvar_tarefas()
            print(f"Tarefa '{tarefa.titulo}' marcada como concluída!")
        else:
            print("Número de tarefa inválido.")

    def remover_tarefa(self, indice: int):
        """Remove a tarefa da lista pelo número/índice."""
        if 1 <= indice <= len(self.tarefas):
            tarefa_removida = self.tarefas.pop(indice - 1)
            self.salvar_tarefas()
            print(f"Tarefa '{tarefa_removida.titulo}' removida com sucesso!")
        else:
            print("Número de tarefa inválido.")

    def salvar_tarefas(self):
        """Salva a lista atual de tarefas no arquivo JSON."""
        dados = [tarefa.para_dicionario() for tarefa in self.tarefas]
        with open(self.arquivo_dados, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=4)

    def carregar_tarefas(self):
        """Carrega as tarefas salvas do arquivo JSON ao iniciar o programa."""
        if os.path.exists(self.arquivo_dados):
            try:
                with open(self.arquivo_dados, "r", encoding="utf-8") as f:
                    dados = json.load(f)
                    self.tarefas = [Tarefa.de_dicionario(d) for d in dados]
            except json.JSONDecodeError:
                self.tarefas = []


def menu():
    gerenciador = GerenciadorTarefas()

    while True:
        print("\n=== GERENCIADOR DE TAREFAS (TODO) ===")
        print("1. Adicionar Tarefa")
        print("2. Listar Tarefas")
        print("3. Concluir Tarefa")
        print("4. Remover Tarefa")
        print("5. Sair")

        opcao = input("Escolha uma opção (1-5): ").strip()

        if opcao == "1":
            titulo = input("Digite a descrição da tarefa: ").strip()
            if titulo:
                gerenciador.adicionar_tarefa(titulo)
            else:
                print("O título não pode estar vazio.")

        elif opcao == "2":
            gerenciador.listar_tarefas()

        elif opcao == "3":
            gerenciador.listar_tarefas()
            if gerenciador.tarefas:
                try:
                    num = int(input("Digite o número da tarefa a concluir: "))
                    gerenciador.concluir_tarefa(num)
                except ValueError:
                    print("Por favor, digite um número válido.")

        elif opcao == "4":
            gerenciador.listar_tarefas()
            if gerenciador.tarefas:
                try:
                    num = int(input("Digite o número da tarefa a remover: "))
                    gerenciador.remover_tarefa(num)
                except ValueError:
                    print("Por favor, digite um número válido.")

        elif opcao == "5":
            print("Saindo do programa... Até mais!")
            break

        else:
            print("Opção inválida! Tente novamente.")

if __name__ == "__main__":
    menu()
