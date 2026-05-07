import sys

def ikili_input(girdi):
    while True:
        val = input(girdi).strip()
        if all(c in '01' for c in val) and len(val) > 0:
            return val
        print("Hata: Girdi yalnızca '0' ve '1' karakterlerini içerebilir.")

def TM_baslat(m1, m2):
    eklenen_sifirlar = "0" * (len(m1) + len(m2) + 1)
    bant_str = f"{m1}*{m2}={eklenen_sifirlar}"
    
    bant = ['B'] * 20 + list(bant_str) + ['B'] * 20
    
    bant_kafasi = 20 
    state = 'q_baslangic'
    adim_sayac = 1

    print("\n" + "="*60)
    print("="*60)
    print(f"Başlangıç Bandı: {bant_str}\n")

    while state not in ['q_bitir', 'q_bitir_sifir']:
        char = bant[bant_kafasi]
        write = char
        move = 'S' # 'S' burada dur demek, geçici bir isarettir.
        next_state = state

        if state == 'q_baslangic':
            if char != '=': move, next_state = 'R', 'q_baslangic'
            else: move, next_state = 'L', 'q_carpan_biti_ara'

        elif state == 'q_carpan_biti_ara':
            if char == '0': write, move, next_state = 'X', 'L', 'q_yildiz_isaretine_git'
            elif char == '1': write, move, next_state = 'X', 'L', 'q_carpilani_ekleme_yolu_gir'
            elif char == 'X': move, next_state = 'L', 'q_carpan_biti_ara'
            elif char == '*': move, next_state = 'L', 'q_sol_tarafi_temizle'


        elif state == 'q_carpilani_ekleme_yolu_gir':
            if char != '*': move = 'L'
            else: move, next_state = 'L', 'q_toplamayi_baslat'

        elif state == 'q_toplamayi_baslat':
            if char in ['a', 'b']: move = 'L'
            elif char == '0': write, move, next_state = 'a', 'R', 'q_0_tasi' 
            elif char == '1': write, move, next_state = 'b', 'R', 'q_1_tasi' 
            elif char == 'B': move, next_state = 'R', 'q_yildizlari_kaldir'

        elif state == 'q_0_tasi':
            if char != 'B': move = 'R'
            else: move, next_state = 'L', 'q_0_icin_yer_ara'

        elif state == 'q_0_icin_yer_ara':
            if char in ['c', 'd']: move = 'L'
            elif char == '0': write, move, next_state = 'c', 'L', 'q_toplama_donusu'
            elif char == '1': write, move, next_state = 'd', 'L', 'q_toplama_donusu'

        elif state == 'q_1_tasi':
            if char != 'B': move = 'R'
            else: move, next_state = 'L', 'q_1_icin_yer_ara'

        elif state == 'q_1_icin_yer_ara':
            if char in ['c', 'd']: move = 'L'
            elif char == '0': write, move, next_state = 'd', 'L', 'q_toplama_donusu'
            elif char == '1': write, move, next_state = 'c', 'L', 'q_elde_1_durumu' 

        elif state == 'q_elde_1_durumu':
            if char == '0': write, move, next_state = '1', 'L', 'q_toplama_donusu'
            elif char == '1': write, move, next_state = '0', 'L', 'q_elde_1_durumu'
            elif char == '=': write, move, next_state = '=', 'L', 'q_elde_1_durumu'

        elif state == 'q_toplama_donusu':
            if char != '*': move = 'L'
            else: move, next_state = 'L', 'q_toplamayi_baslat'

        elif state == 'q_yildizlari_kaldir':
            if char == 'a': write, move = '0', 'R'
            elif char == 'b': write, move = '1', 'R'
            elif char == 'c': write, move = '0', 'R'
            elif char == 'd': write, move = '1', 'R'
            elif char in ['0', '1', 'X', '*', '=']: move = 'R'
            elif char == 'B': move, next_state = 'L', 'q_yildiz_isaretine_git'


        elif state == 'q_yildiz_isaretine_git':
            if char != '*': move = 'L'
            else: move, next_state = 'L', 'q_0_kaydir'

        elif state == 'q_0_kaydir':
            if char == '0': write, move = '0', 'L'
            elif char == '1': write, move, next_state = '0', 'L', 'q_1_kaydir'
            elif char == 'B': write, move, next_state = '0', 'R', 'q_esittir_don'

        elif state == 'q_1_kaydir':
            if char == '0': write, move, next_state = '1', 'L', 'q_0_kaydir'
            elif char == '1': write, move = '1', 'L'
            elif char == 'B': write, move, next_state = '1', 'R', 'q_esittir_don'

        elif state == 'q_esittir_don':
            if char != '=': move = 'R'
            else: move, next_state = 'L', 'q_carpan_biti_ara'


        elif state == 'q_sol_tarafi_temizle':
            if char != 'B': write, move = 'B', 'L'
            else: move, next_state = 'R', 'q_sag_tarafi_temizle'

        elif state == 'q_sag_tarafi_temizle':
            if char == 'B': move = 'R'
            elif char in ['*', 'X']: write, move = 'B', 'R'
            elif char == '=': write, move, next_state = 'B', 'R', 'q_sifirlari_temizle_bitir'

        elif state == 'q_sifirlari_temizle_bitir':
            if char == '0': write, move = 'B', 'R'
            elif char == '1': next_state = 'q_bitir'
            elif char == 'B': move, next_state = 'L', 'q_bitir_sifir'

        bant_goruntule = "".join(bant).strip('B')
        print(f"Adım {adim_sayac:04d} | Durum: {state:<27s} | Okunan: {char} | Yazılan: {write} | Hareket: {move} | Bant: {bant_goruntule}")

        bant[bant_kafasi] = write
        if move == 'R': bant_kafasi += 1
        elif move == 'L': bant_kafasi -= 1
        state = next_state
        adim_sayac += 1

    final_bant = "".join(bant).replace('B', '')
    if state == 'q_bitir_sifir' or final_bant == '':
        final_bant = '0'

    return final_bant

if __name__ == "__main__":
    print("--- Turing Makinesi İle İkili (Binary) Çarpma ---")
    carpilan = ikili_input("Birinci binary sayıyı giriniz (Çarpılan): ")
    carpan = ikili_input("İkinci binary sayıyı giriniz (Çarpan): ")
    
    final_binary = TM_baslat(carpilan, carpan)
    final_decimal = int(final_binary, 2)
    
    print("\n" + "="*60)
    print(" SONUÇ")
    print("="*60)
    print(f"Binary Sonuç  : {final_binary}")
    print(f"Decimal Sonuç : {final_decimal}")
    print("="*60)
