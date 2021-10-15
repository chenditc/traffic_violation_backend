import styles from "@/pages/index.less";
import { useState, useCallback } from "react";
import { Space, Input, Button, List } from "antd-mobile";
import { history } from "umi";
const fullHeight = {
  height: "100%",
};
export default function LoginPage() {
  const [phoneNumber, setPhoneNumber] = useState("");
  const onPhoneNumberChange = useCallback(
    (value) => {
      setPhoneNumber(value);
    },
    [setPhoneNumber],
  );
  const onLogin = useCallback(() => {
    // TODO verify login info
    if (true) {
      history.push("/list");
    }
  }, []);
  // TODO validate phone number
  return (
    <div className={styles["center-layout"]} style={fullHeight}>
      <Space direction="vertical" className={styles["phone-input-area"]}>
        <Input
          type="phone"
          clearable={true}
          value={phoneNumber}
          onChange={onPhoneNumberChange}
          placeholder="Input phone number"
          className={styles["phone-input"]}
        />
        <Button
          onClick={onLogin}
          className={styles["login-button"]}
          size="large"
        >
          Login
        </Button>
      </Space>
    </div>
  );
}
