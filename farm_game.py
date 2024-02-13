import time
import os
import json

class FarmGame:
    def __init__(self):
        self.money = 0
        self.grains = 0
        self.seeds = 5
        self.available_areas = 2
        self.occupied_areas = []
        self.plants = {}

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_menu(self):
        self.clear_screen()
        print("===== Fazenda do Jogador =====")
        print(f"Dinheiro: ${self.money}")
        print(f"Grãos: {self.grains}")
        print(f"Sementes: {self.seeds}")
        print(f"Áreas Disponíveis: {self.available_areas}")
        print("Áreas Ocupadas:")
        for area_id, plant in self.plants.items():
            print(f"  Área {area_id}: {plant['stage']}")
        print("\n===== Menu =====")
        print("1. Plantar Semente")
        print("2. Colher Todas as Plantas Prontas")
        print("3. Comprar Sementes")
        print("4. Comprar Área")
        print("5. Vender Grãos")
        print("6. Salvar Jogo")
        print("7. Carregar Jogo")
        print("8. Sair")

    def plant_seed(self):
        if self.seeds > 0 and self.available_areas > 0:
            area_id = max(self.occupied_areas) + 1 if self.occupied_areas else 1
            self.occupied_areas.append(area_id)
            self.available_areas -= 1
            self.seeds -= 1
            self.plants[area_id] = {'stage': 'Nascendo', 'time_planted': time.time()}
            print(f"[!] Semente plantada na Área {area_id}")
        elif self.seeds == 0:
            print("[!] Não há sementes disponíveis.")
        elif self.available_areas == 0:
            print("[!] Não há áreas disponíveis para plantio.")
        time.sleep(3)

    def harvest_all_crops(self):
        harvested_areas = []
        for area_id, plant in self.plants.items():
            if plant['stage'] == 'Pronto para Colheita':
                harvested_areas.append(area_id)
                self.grains += area_id * 5  # Valor arbitrário de grãos por área

        for area_id in harvested_areas:
            del self.plants[area_id]
            self.occupied_areas.remove(area_id)
            self.available_areas += 1

        if not harvested_areas:
            print("[!] Nenhuma planta pronta para colheita.")
        time.sleep(3)

    def sell_grains(self):
        if self.grains > 0:
            money_earned = self.grains * 2  # Valor arbitrário de venda de grãos
            self.money += money_earned
            self.grains = 0
            print(f"[!] Você vendeu {self.grains} grãos por ${money_earned}.")
        else:
            print("[!] Não há grãos para vender.")
        time.sleep(3)

    def buy_seeds(self):
        cost = 5  # Custo arbitrário por semente
        if self.money >= cost:
            self.money -= cost
            self.seeds += 1
            print("[!] Você comprou uma semente.")
        else:
            print("[!] Dinheiro insuficiente para comprar semente.")
        time.sleep(3)

    def buy_area(self):
        cost = 20  # Custo arbitrário por área
        if self.money >= cost:
            self.money -= cost
            self.available_areas += 1
            print("[!] Você comprou uma área.")
        else:
            print("[!] Dinheiro insuficiente para comprar área.")
        time.sleep(3)

    def update_plants(self):
        current_time = time.time()
        for area_id, plant in self.plants.items():
            time_elapsed = current_time - plant['time_planted']
            if time_elapsed >= 30:
                stages = ['Nascendo', 'Criando Grãos', 'Secando', 'Pronto para Colheita']
                current_stage_index = int(time_elapsed // 30)
                plant['stage'] = stages[current_stage_index]

    def save_game(self, filename='savegame.json'):
        data = {
            'money': self.money,
            'grains': self.grains,
            'seeds': self.seeds,
            'available_areas': self.available_areas,
            'occupied_areas': self.occupied_areas,
            'plants': self.plants
        }
        with open(filename, 'w') as file:
            json.dump(data, file)
        print("[!] Jogo salvo com sucesso.")

    def load_game(self, filename='savegame.json'):
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
            self.money = data['money']
            self.grains = data['grains']
            self.seeds = data['seeds']
            self.available_areas = data['available_areas']
            self.occupied_areas = data['occupied_areas']
            self.plants = data['plants']
            print("[!] ogo carregado com sucesso.")
        except FileNotFoundError:
            print("[!] Arquivo de savegame não encontrado.")
        except json.JSONDecodeError:
            print("[!] Erro ao decodificar o arquivo de savegame.")

    def game_loop(self):
        while True:
            self.update_plants()
            self.print_menu()
            choice = input("[>] Escolha uma opção: ")

            if choice == '1':
                self.plant_seed()
            elif choice == '2':
                self.harvest_all_crops()
            elif choice == '3':
                self.buy_seeds()
            elif choice == '4':
                self.buy_area()
            elif choice == '5':
                self.sell_grains()
            elif choice == '6':
                self.save_game()
            elif choice == '7':
                self.load_game()
            elif choice == '8':
                print("Obrigado por jogar! Até mais.")
                break
            else:
                print("[!] Opção inválida. Tente novamente.")
            time.sleep(3)

if __name__ == "__main__":
    game = FarmGame()
    game.game_loop()