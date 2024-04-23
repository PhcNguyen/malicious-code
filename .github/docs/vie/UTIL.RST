.. function:: Sub_Bytes(s: List[List[int]]) -> None

   Thực hiện thay thế từng byte của ma trận đầu vào ``s`` bằng các giá trị trong ``s_box``.

.. function:: inv_Sub_Bytes(s: List[List[int]]) -> None

   Thực hiện thay thế từng byte của ma trận đầu vào ``s`` bằng các giá trị trong ``inv_s_box``.

.. function:: Shift_Rows(s: List[List[int]]) -> None

   Dịch các hàng của ma trận đầu vào ``s`` sang trái dựa trên vị trí của hàng.

.. function:: inv_Shift_Rows(s: List[List[int]]) -> None

   Dịch các hàng của ma trận đầu vào ``s`` sang phải dựa trên vị trí của hàng.

.. function:: add_Round_Key(s: List[List[int]], k: List[List[int]]) -> None

   Thực hiện phép XOR giữa mỗi phần tử tương ứng của hai ma trận đầu vào ``s`` và ``k``.

.. function:: Mix_Single_Column(a: List[int]) -> None

   Thực hiện phép trộn trên một cột (1D array) đầu vào ``a``.

.. function:: Mix_Columns(s: List[List[int]]) -> None

   Thực hiện phép trộn trên tất cả các cột của ma trận đầu vào ``s``.

.. function:: inv_Mix_Columns(s: List[List[int]]) -> None

   Thực hiện phép trộn ngược lại trên tất cả các cột của ma trận đầu vào ``s``.

.. function:: Bytes2Matrix(text: bytes) -> List[List[int]]

   Chuyển đổi dữ liệu bytes thành ma trận 4x4.

.. function:: Matrix2Bytes(matrix: List[List[int]]) -> bytes

   Chuyển đổi ma trận 4x4 thành dữ liệu bytes.

.. function:: xor_Bytes(a: bytes, b: bytes) -> bytes

   Thực hiện phép XOR giữa hai dữ liệu bytes đầu vào ``a`` và ``b``.

.. function:: inc_Bytes(a: bytes) -> bytes

   Tăng giá trị của dữ liệu bytes đầu vào ``a`` lên một.

.. function:: Split_Blocks(message: bytes, block_size: int = 16, require_padding: bool = True) -> List[BLOCK]

   Chia dữ liệu bytes thành các khối có độ dài ``block_size`` và trả về một danh sách các khối.

.. function:: GET_KEY_IV(password: bytes, salt: SALT) -> Tuple[KEY, KEY, IV]

   Tạo các khóa và vector khởi tạo từ mật khẩu và muối đầu vào.
