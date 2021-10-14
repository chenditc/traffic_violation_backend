import styles from '@/pages/index.less';
import {
  useState,
  useCallback,
} from "react"
import { WhiteSpace, InputItem, Button } from 'antd-mobile';
import { history } from 'umi';
const fullHeight = {
  height: '100%',
};
export default function LoginPage() {
  const [phoneNumber, setPhoneNumber] = useState('');
  const onPhoneNumberChange = useCallback(
    (value) => {
      setPhoneNumber(value);
    },
    [setPhoneNumber],
  );
  const onLogin = useCallback(() => {
    // TODO verify login info
    if (true) {
      history.push('/list');
    }
  }, []);
  // TODO validate phone number
  return (
    <div className={styles['center-layout']} style={fullHeight}>
      <div className={styles['phone-input']}>
      <InputItem
        type="phone"
        clear={true}
        value={phoneNumber}
        onChange={onPhoneNumberChange}
        placeholder="Input phone number"
      />
      <WhiteSpace />
      <Button onClick={onLogin}>Login with phone number</Button>
      </div>
    </div>
  );
}
