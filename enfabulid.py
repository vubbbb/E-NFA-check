class ENFA:
    def __init__(self, num_states, alphabet):
        self.states = list(range(num_states))  # danh sách trạng thái
        self.alphabet = alphabet  # bảng chữ cái đầu vào
        self.transition = {}  # hàm chuyển trạng thái (tự điển)
        self.start_state = 0  # trạng thái bắt đầu
        self.final_states = set()  # tập trạng thái kết thúc

    def add_transition(self, state, symbol, next_states):
        """Thêm quy tắc chuyển trạng thái từ trạng thái 'state'
          qua ký tự 'symbol' đến tập trạng thái 'next_states'."""
        if (state, symbol) in self.transition:
            self.transition[(state, symbol)].extend(next_states)
        else:
            self.transition[(state, symbol)] = next_states
    
    def add_final_state(self, state):
        """Thêm trạng thái 'state' vào tập trạng thái kết thúc."""
        self.final_states.add(state)

    def epsilon_closure(self, states):
        """Tính tập đóng epsilon của các trạng thái trong 'states'."""
        closure = set(states)
        temp = list(states)
        while temp:
            state = temp.pop()
            if (state, '*') in self.transition:
                for next_state in self.transition[(state, '*')]:
                    if next_state not in closure:
                        closure.add(next_state)
                        temp.append(next_state)
        return (closure)

    def move(self, states, symbol):
        """Tính tập trạng thái đến được từ các trạng thái trong 'states'
          qua ký tự 'symbol'."""
        next_states = set()
        for state in states:
            if (state, symbol) in self.transition:
                next_states.update(self.transition[(state, symbol)])
        return frozenset(next_states)

    def accept(self, string):
        """Kiểm tra xem chuỗi 'string' có được chấp nhận bởi E-NFA hay không."""
        current_states = self.epsilon_closure({self.start_state})
        for symbol in string:
            current_states = self.epsilon_closure(self.move(current_states, symbol))
        return bool(current_states.intersection(self.final_states))

# Đọc dữ liệu từ tệp tin
print("------ CHƯƠNG TRÌNH XÂY DỰNG NFA-E VÀ KIỂM TRA CHUỖI NHẬP VÀO ------")
with open('data1.txt') as f:
    num_states = int(f.readline())
    enfa = ENFA(num_states, f.readline().split())
    for line in f:
        charlist = line.split()
        if charlist[0] == '*':
          final_states = charlist[1:]
          for final_state in final_states:
            enfa.add_final_state(int(final_state))            
        else:
            src, symbol, dest = line.split()
            enfa.add_transition(int(src), symbol, [int(dest)])
    print("Bảng chữ cái đầu vào: ", enfa.alphabet)
    print("Trạng thái kết thúc:",enfa.final_states)
    print("Tất cả các hàm chuyển trạng thái", enfa.transition)
# Sử dụng E-NFA để kiểm tra chuỗi
stateCheck = set()
stateCheck.add(2)
closure =  enfa.epsilon_closure(stateCheck)
print("epsilon closure của", stateCheck, ": ", closure)


string = input('Nhập chuỗi đầu vào: ')
if enfa.accept(string):
    print('Chuỗi được chấp nhận bởi NFA-E.')
else:
    print('Chuỗi không được chấp nhận bởi NFA-E.')