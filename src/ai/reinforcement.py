import random
import numpy as np

class QLearningAgent:
    """
    Đại diện cho một tác nhân học tăng cường (Reinforcement Learning) sử dụng thuật toán Q-Learning.
    """
    def __init__(self, state_space, action_space, learning_rate=0.1, discount_factor=0.9, exploration_rate=1.0, exploration_decay=0.99):
        """
        Khởi tạo tác nhân Q-Learning.
        :param state_space: Số lượng trạng thái có thể có.
        :param action_space: Số lượng hành động có thể thực hiện.
        :param learning_rate: Tốc độ học (alpha).
        :param discount_factor: Hệ số chiết khấu (gamma).
        :param exploration_rate: Tỷ lệ khám phá ban đầu (epsilon).
        :param exploration_decay: Tỷ lệ giảm epsilon sau mỗi bước.
        """
        self.state_space = state_space
        self.action_space = action_space
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.exploration_decay = exploration_decay
        self.q_table = np.zeros((state_space, action_space))  # Bảng Q ban đầu

    def choose_action(self, state):
        """
        Chọn hành động dựa trên chính sách epsilon-greedy.
        :param state: Trạng thái hiện tại.
        :return: Hành động được chọn.
        """
        if random.uniform(0, 1) < self.exploration_rate:
            return random.randint(0, self.action_space - 1)  # Chọn hành động ngẫu nhiên
        else:
            return np.argmax(self.q_table[state])  # Chọn hành động tốt nhất dựa trên Q-Table

    def update_q_value(self, state, action, reward, next_state):
        """
        Cập nhật giá trị Q cho trạng thái và hành động hiện tại.
        :param state: Trạng thái hiện tại.
        :param action: Hành động đã thực hiện.
        :param reward: Phần thưởng nhận được.
        :param next_state: Trạng thái tiếp theo.
        """
        best_next_action = np.argmax(self.q_table[next_state])
        td_target = reward + self.discount_factor * self.q_table[next_state][best_next_action]
        td_error = td_target - self.q_table[state][action]
        self.q_table[state][action] += self.learning_rate * td_error

    def decay_exploration(self):
        """
        Giảm tỷ lệ khám phá (epsilon) sau mỗi bước.
        """
        self.exploration_rate *= self.exploration_decay
        self.exploration_rate = max(self.exploration_rate, 0.01)  # Đảm bảo epsilon không giảm dưới 0.01


