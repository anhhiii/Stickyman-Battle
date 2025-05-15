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
  ** 
- BFS là lựa chọn ưu việt khi cần đảm bảo tính chính xác và toàn diện trong việc tìm đường, nhưng kém hiệu quả khi không gian trạng thái lớn hoặc có trọng số đa dạng.
- Q-Learning mang lại khả năng học hỏi và thích nghi, phù hợp với môi trường chiến đấu biến đổi và tăng tính đa dạng hành vi.
- Greedy Search cung cấp phản ứng nhanh, phù hợp các tình huống yêu cầu tốc độ hơn độ chính xác.
- Backtracking và And-Or Search thích hợp cho các bài toán ra quyết định phức tạp, xử lý đa nhánh và nhiều điều kiện.
- Hill Climbing là công cụ hiệu quả cho các quyết định tối ưu cục bộ, nhanh nhưng cần kết hợp với các thuật toán khác để tránh mắc kẹt.

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
- assets        # Tài nguyên hình ảnh, âm thanh
- maps          # File bản đồ .tmx
- src           # Mã nguồn game và AI
- main.py       # File chạy chính
- README.md     # Tệp hướng dẫn này

---
## DEMO
- Màn hình Start game <br>
![Màn hình Start game](https://drive.google.com/uc?export=view&id=1tmrfYMf8bXFAwjqoaOx9CSzzTHhWYamr)

- Màn hình Level 1 <br>
![Màn hình Level 1](https://drive.google.com/uc?export=view&id=1N6b_rr1CJldaqouGwajteCOM0-r5JoFb)

- Màn hình Game over <br>
![Màn hình Game over](https://drive.google.com/uc?export=view&id=1eY63pPhHLE09zdcsVAv_lI3yYsekZYe5)

- Màn hình Win game <br>
![Màn hình Win game](https://drive.google.com/uc?export=view&id=1L7dykpLmH6X-8GgWjtG8ZcDB4yU_7OQF)

---
## Kết quả và đánh giá
- Game chạy ổn định, không gặp lỗi.
- Nhân vật chính di chuyển, nhảy, tấn công mượt mà, va chạm hợp lý với môi trường.
- Camera theo sát nhân vật mượt mà không bị lag.
- AI Slime có hành vi linh hoạt, truy đuổi và phản ứng hợp lý với nhân vật Stickman.
- Giao diện game trực quan, thân thiện với người chơi.

## Những khó khăn gặp phải
- Sai lệch trong tính toán camera_offset dẫn đến bản đồ bị lệch khi hiển thị.
- Xử lý va chạm phức tạp giữa các đối tượng, đặc biệt khi nhân vật nhảy hoặc leo bậc thang.
- Đồng bộ hoạt ảnh khi tấn công hoặc chuyển trạng thái không mượt do frame animation chưa tối ưu.
- Khó xác định mặt đất chính xác khi bản đồ có nhiều layer chồng lên nhau.

## Định hướng phát triển tiếp theo
- Thêm hệ thống HUD hiển thị thanh máu, tên nhân vật, chỉ số kỹ năng theo thời gian thực.
- Phát triển thêm nhiều màn chơi, đa dạng bản đồ, hỗ trợ chuyển cảnh (portal/door).
- Nâng cao AI Slime để có thể tự động di chuyển, tấn công, phòng thủ theo phạm vi.
- Cải thiện vật lý game như nhảy, leo thang, xử lý va chạm góc cạnh thực tế hơn.
- Tối ưu hiệu suất để giảm flickering và tăng tốc độ render.

## Tài liệu tham khảo
 - [StickMan_Game GitHub](https://github.com/nguyenhuytlu/StickMan_Game)
 - [StickMan Game Development Series YouTube Playlist](https://www.youtube.com/playlist?list=PLjcN1EyupaQm20hlUE11y9y8EY2aXLpnv)

---
## NHÓM SINH VIÊN THỰC HIỆN: NHÓM 06
 - Nguyễn Thanh Khang	- 23110237
 - Đoàn Thị Thu Trang	- 23110347
 - Nguyễn Tấn Yên	- 23110369

