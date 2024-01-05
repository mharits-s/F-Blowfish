# F-Blowfish (Optimized Blowfish with F-Function Modification)
 ![Information and Network Security](https://github.com/mharits-s/F-Blowfish/blob/main/assets/information%20and%20network%20security.svg?raw=true)
 
Implementasi Teknik Enkripsi Blowfish yang Dioptimalkan dengan Modifikasi F Function

## Overview

F-Blowfish is an implementation of the Blowfish encryption algorithm with an optimized F-function modification. The Blowfish algorithm is a symmetric-key block cipher designed by Bruce Schneier in 1993. This implementation introduces an optimized F-function for improved performance.

## Features

- **Optimized F-Function:** The F-function, responsible for the confusion in Blowfish, has been optimized for efficiency.

- **Subkey Generation:** The algorithm generates subkeys dynamically based on the provided key.

- **Padding:** Text input is padded to ensure proper block processing during encryption.

- **Encryption:** The provided text input is encrypted using the F-Blowfish algorithm.

- **Decryption:** The encrypted data can be decrypted to retrieve the original text.

## How to Use

1. **Installation:**
   - Clone the repository to your local machine.

2. **Dependencies:**
   - Ensure that you have the required dependencies installed. (Check the `constants` module for any specific dependencies)

3. **Run the Code:**
   - Execute the `driver()` function in the main script.

4. **Input:**
   - Enter the text you want to encrypt when prompted.

5. **Output:**
   - The encrypted data in hexadecimal format will be displayed, along with the encryption time.

   - The decrypted data and decryption time will also be presented.

## Sample Usage

```python
# Main
if __name__ == "__main__":
    driver()
```

## Performance

- **Encryption Time:**
  - The time taken to encrypt the input data is displayed in milliseconds.

- **Decryption Time:**
  - The time taken to decrypt the encrypted data is displayed in milliseconds.

## Contribution

Contributions to optimize the algorithm further or enhance its features are welcome. Please follow the standard GitHub workflow:

1. Fork the repository.
2. Create a new branch.
3. Make changes and commit them.
4. Push the changes to your fork.
5. Create a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

---

Feel free to use and contribute to F-Blowfish! If you have any questions or suggestions, please open an issue.
