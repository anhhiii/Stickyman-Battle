# Stickman Battle

## Giới thiệu
**Stickman Battle** là trò chơi hành động 2D. Người chơi điều khiển nhân vật Stickman chiến đấu với các quái vật trong các màn chơi đa dạng, với hệ thống AI hỗ trợ di chuyển và chiến đấu thông minh. Trò chơi ứng dụng các thuật toán trí tuệ nhân tạo (AI) để tối ưu hóa hành vi nhân vật và kẻ địch, mang lại trải nghiệm chơi mượt mà, thử thách và hấp dẫn.

---

## Tính năng nổi bật
- Nhân vật Stickman có thể di chuyển, nhảy, tấn công và phòng thủ với hoạt ảnh mượt mà.
- Quái vật tự động di chuyển, truy đuổi người chơi nhờ các thuật toán tìm đường thông minh.
- Hệ thống nâng cấp vũ khí thông minh dựa trên thuật toán Decision Tree.
- Bản đồ game đọc từ file `.tmx` đa layer, tạo môi trường chơi phong phú.
- Camera theo sát nhân vật, giao diện trực quan, thân thiện với người dùng.

---

## Công nghệ sử dụng
- Ngôn ngữ: **Python 3.10+**
- Thư viện:
  - [Pygame](https://www.pygame.org/) - phát triển game 2D
  - [pytmx](https://github.com/bitcraft/pytmx) - đọc file bản đồ `.tmx`
  - [NumPy](https://numpy.org/) - xử lý toán học, khoảng cách
  - [Matplotlib](https://matplotlib.org/) - hỗ trợ phân tích (ngoài game)
- IDE gợi ý: Visual Studio Code, PyCharm

---

## Các thuật toán AI pathfinding và hành vi sử dụng trong game
Trong game Stickman Battle, các thuật toán trí tuệ nhân tạo được sử dụng để điều khiển hành vi di chuyển và chiến đấu của nhân vật và quái vật, gồm:
1. **BFS (Breadth-First Search)**  
   Tìm đường đi ngắn nhất trong môi trường grid không trọng số, dùng để truy đuổi hoặc di chuyển an toàn.
2. **Greedy Best-First Search**  
   Sử dụng heuristic Manhattan để đi nhanh về đích, hiệu quả trong tìm đường với chi phí thấp.
3. **Hill Climbing Step**  
   Tính bước di chuyển tiếp theo dựa trên giảm thiểu khoảng cách đến đích, đơn giản và nhanh gọn.
4. **Backtracking Pathfinding**  
   Tìm đường đi bằng phương pháp đệ quy quay lui, thích hợp cho môi trường nhỏ hoặc khi cần tìm tất cả đường đi.
5. **Q-Learning**  
   Thuật toán học củng cố giúp nhân vật học dần cách chọn hành động tối ưu qua các lần chơi, tăng khả năng tự thích nghi.
6. **And-Or Search**  
   Tìm kiếm dạng cây quyết định, dùng trong môi trường phức tạp, đảm bảo không bỏ sót lựa chọn.

---

## Hướng dẫn cài đặt và chạy game
1. Cài đặt thư viện cần thiết:
   ```bash
   pip install pygame pytmx base64
2. Chạy game:
   ```bash
   python main.py
 
---
## Cấu trúc thư mục
/assets        # Tài nguyên hình ảnh, âm thanh
/maps          # File bản đồ .tmx
/src           # Mã nguồn game và AI
main.py       # File chạy chính
README.md     # Tệp hướng dẫn này

---


