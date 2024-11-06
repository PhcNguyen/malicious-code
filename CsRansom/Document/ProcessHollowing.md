# How to Use the Process Hollowing Technique

> [!WARNING]
> **Sử dụng có trách nhiệm:**
> - Kỹ thuật này có thể được sử dụng cho mục đích xấu. 
> - Hãy đảm bảo bạn hiểu rõ và tuân thủ luật pháp và quy định liên quan đến bảo mật phần mềm.
>
> **Kiến thức về bảo mật:**
> - Để sử dụng thành công kỹ thuật này, bạn cần có kiến thức vững về lập trình, 
>   bảo mật và hoạt động của hệ thống.

## Introduce
Lớp `ProcessHollowing` cho phép bạn thực hiện kỹ thuật hollowing, tức là tải mã vào một tiến trình hiện có. Kỹ thuật này thường được sử dụng trong lĩnh vực bảo mật để kiểm tra hoặc nghiên cứu phần mềm độc hại, nhưng cần được sử dụng cẩn thận và hợp pháp.

## How to use

1. **Tạo một instance của lớp `ProcessHollowing`**: Bạn cần chỉ định ID của tiến trình mục tiêu và mã shellcode mà bạn muốn thực thi.

2. **Gọi phương thức `Execute`**: Phương thức này sẽ thực hiện quá trình hollowing và chạy mã shellcode trong tiến trình mục tiêu.

### Example

```csharp
class Program
{
    static void Main()
    {
        // Mã shellcode (thay thế bằng mã thực tế bạn muốn chạy)
        byte[] shellcode = new byte[] { /* Your shellcode here */ };
        
        // ID tiến trình mục tiêu (thay thế bằng ID thực tế)
        int targetProcessId = 1234; // ID của tiến trình mà bạn muốn thực hiện hollowing

        // Tạo một đối tượng ProcessHollowing và thực hiện hollowing
        var processHollowing = new ProcessHollowing(targetProcessId, shellcode);
        processHollowing.Execute();
    }
}
```

### Notes

- Đảm bảo thay thế mã shellcode bằng mã hợp lệ mà bạn muốn thực thi.
- Thay thế ID tiến trình mục tiêu bằng ID thực tế mà bạn muốn thao tác.
- Lưu ý rằng việc sử dụng kỹ thuật này có thể vi phạm pháp luật nếu không được thực hiện đúng cách, vì vậy hãy cẩn thận và sử dụng trong môi trường hợp pháp.

> [!NOTE]  
> **Cách lấy Shellcode**
> 1. **Sử dụng công cụ tạo Shellcode**
>    - **MSFVenom**: Cho phép tạo `Shellcode` bằng nhiều ngôn ngữ khác nhau và cho nhiều hệ điều hành.
>    - **Donut**: Một công cụ để tạo `Shellcode` từ các tệp PE (.exe, .dll) và .NET Assemblies. Bạn có thể tải Donut từ GitHub và sử dụng để tạo `Shellcode` cho C#.
>
> 2. **Tạo Shellcode trực tiếp từ mã Assembly**
>    - Nếu bạn muốn tự viết `Shellcode`, bạn có thể biên dịch mã Assembly thành mã máy và sử dụng trong ứng dụng.
> 
>    - Example:
>
>       ```assembly
>       ; Assembly code for a basic MessageBox (Windows x64)
>       mov r9, 0 ; MessageBox type
>       lea r8, [msgBoxText] ; Text
>       lea rdx, [msgBoxCaption] ; Caption
>       mov rcx, 0 ; Handle
>       call MessageBoxA
>       ```
>     - Biên dịch mã Assembly này để lấy `Shellcode`, sau đó chèn vào mã C# của bạn.

## Contacts

If you have any questions, please reach out to the developers at **PhcNguyen Developers**.

You can also contact me via Telegram: [phcnguyenz](https://t.me/phcnguyenz).