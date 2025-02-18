class RC4Kit:
    @staticmethod
    def encrypt(data, key):
        encrypted_bytes = RC4Kit.base(data.encode("utf-8"), key)
        return RC4Kit.bytes_to_hex_string(encrypted_bytes)

    @staticmethod
    def decrypt(data, key):
        decrypted_bytes = RC4Kit.base(RC4Kit.hex_string_to_bytes(data), key)
        try:
            return decrypted_bytes.decode("utf-8")
        except UnicodeDecodeError:
            try:
                return decrypted_bytes.decode("latin-1")  # Attempt to decode using latin-1
            except UnicodeDecodeError:
                return decrypted_bytes  # Return raw bytes if decoding fails

    @staticmethod
    def base(data, key):
        key_bytes = [ord(c) for c in key]
        state = list(range(256))
        index1 = 0
        index2 = 0

        for i in range(256):
            index2 = (key_bytes[index1] + state[i] + index2) & 0xFF
            state[i], state[index2] = state[index2], state[i]
            index1 = (index1 + 1) % len(key_bytes)

        x = 0
        y = 0
        output = bytearray()
        for byte in data:
            x = (x + 1) & 0xFF
            y = (state[x] + y) & 0xFF
            state[x], state[y] = state[y], state[x]
            output.append(byte ^ state[(state[x] + state[y]) & 0xFF])

        return output

    @staticmethod
    def hex_string_to_bytes(hex_string):
        return bytes.fromhex(hex_string)

    @staticmethod
    def bytes_to_hex_string(byte_data):
        return byte_data.hex()


# 示例用法
if __name__ == "__main__":
    # 接口返回值
    encode_result = "AC809486F0D2B825A9F7067583C5D15AB017F27BCDDEA0138390A9E4FF3FFC5707D9DB4A2FB65E399D10F671B6C0186E60A717C95E9082BC2FB9FAEDCF3D8A60F57344ACCA8A222CD858776DFAF35C53BAC44A75B6C820166DEEA405FBE45730C4784F711D763C6F111EBF7A4F7F7B466C7F44C552502085458B350B53E0E9476F1447337D24FA00362C7D5DA22E0464D273D65C4875036260A47B734CECE43A6B040AF546386A8F1BEC6D0CF708C3884E696116445B627892308E54DF3493EE5A73E76A6F00849983E1422031E0C3698E32486EF78C04ED297382BDA2631FF5E18A3A34DBF82D8906F16CDBF70E7786D6FBD2FE4CD076563BCAE59307C0FEBBB2796D51D3CAEF7BBBD207B887353B78310B9B63C5B6AEDEBD2FAF042DDE4AC613CAD51879A94484CA972422ED0CF1589485074124A55EAEAC11E5ACC30CFA2986374FE31625FB31F8B0626038A37829CDF6259F844E037311355A47F7832FC1B5CCBA8346F027D997CD53B8990BE4515B6A3C69AA90F9799AF0C217B1D70ED2BD83C656477A0D2D23F7AB8496ADE7CB0F09A2B55AA540C3487B0AEFBC58ED7EFC6427DC47DA0F27FF0087BF9EA0801ADF0466B1D262720BDEC305BAB7DF8DFB510E0C795628BB193F70B6EDED649A5CC0AC347343805A3150D9BA4E6FA1123F3B3749FB111AC69D89EBA44723594E4341E8085F4317ABAD91E839E89E51E59750A9C46300FE433F4D4127980AD50184A8770483CDF75864E041B2C7CD6DD77A81B8FF0C6795DE68ACB065ECD475ABCD0B9F85218D1FEC5A938C564BDF419C77F51006F2672B80CF2F70A287611B3C81703A32B181DE28C4B5B7904CB57B1C151AD2E3EEFD0C67F18D06847C886497CFECF4EDB9B36DF572839AEE1B0ED6C2F29F3790CCF7CB1025EF05AA7DCFA7615BC8F17F56BBB4A137CC0DD263FED2317349D1972E1D919D5F6ECD05BE010C632F0228F0CDD54700357BCA1003B73B6E04D86585DB380A11F38A8877BABFA766E803FC4EA0F8948F890849B8CE2D0DBD11CC2F4291C7EF97096EA03AC495FB7FEA515E9196F1571CD4E1233695B4325E21B8DB2B840C6315F6C9ED8858966B6715512A219486D2695A12227EDB4CDC6D8F760837AE5A1740242AAE7C607FB2C32101"
    # 密钥
    # TODO app首次启动,会动态生成,后续app要增加获取方案
    key = "abcdefghijklmnopqrstuvwxyzABCDEF"

    print(f"Encode: {encode_result}")
    decrypted = RC4Kit.decrypt(
        encode_result,
        key,
    )
    print(f"Decrypted: {decrypted}")
    encrypted = RC4Kit.encrypt(decrypted, key)
    print(f"Ecnrypted 2: {encrypted}")
    decrypted = RC4Kit.decrypt(
        encrypted,
        key,
    )
    print(f"Decrypted 2: {decrypted}")

    print(f"encrypt_result == encode_result {encrypted.lower() == encode_result.lower()}")
