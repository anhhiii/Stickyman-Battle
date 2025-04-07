class State:
    """
    Đại diện cho một trạng thái trong máy trạng thái.
    """
    def __init__(self, name):
        """
        Khởi tạo trạng thái.
        :param name: Tên của trạng thái.
        """
        self.name = name

    def enter(self, entity):
        """
        Hàm được gọi khi thực thể (entity) chuyển sang trạng thái này.
        :param entity: Thực thể đang chuyển trạng thái.
        """
        pass

    def execute(self, entity):
        """
        Hàm được gọi để thực thi logic của trạng thái.
        :param entity: Thực thể đang ở trạng thái này.
        """
        pass

    def exit(self, entity):
        """
        Hàm được gọi khi thực thể rời khỏi trạng thái này.
        :param entity: Thực thể đang rời khỏi trạng thái.
        """
        pass


class StateMachine:
    """
    Máy trạng thái để quản lý các trạng thái của thực thể.
    """
    def __init__(self, entity):
        """
        Khởi tạo máy trạng thái.
        :param entity: Thực thể được quản lý bởi máy trạng thái.
        """
        self.entity = entity
        self.current_state = None
        self.previous_state = None
        self.global_state = None

    def set_global_state(self, state):
        """
        Thiết lập trạng thái toàn cục (global state).
        :param state: Trạng thái toàn cục.
        """
        self.global_state = state

    def change_state(self, new_state):
        """
        Chuyển sang trạng thái mới.
        :param new_state: Trạng thái mới.
        """
        if self.current_state:
            self.current_state.exit(self.entity)  # Gọi hàm thoát của trạng thái hiện tại
        self.previous_state = self.current_state
        self.current_state = new_state
        self.current_state.enter(self.entity)  # Gọi hàm vào của trạng thái mới

    def revert_to_previous_state(self):
        """
        Quay lại trạng thái trước đó.
        """
        if self.previous_state:
            self.change_state(self.previous_state)

    def update(self):
        """
        Cập nhật máy trạng thái, thực thi logic của trạng thái hiện tại và trạng thái toàn cục.
        """
        if self.global_state:
            self.global_state.execute(self.entity)
        if self.current_state:
            self.current_state.execute(self.entity)


