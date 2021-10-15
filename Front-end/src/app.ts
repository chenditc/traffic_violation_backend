import { RequestConfig } from "umi";
export const request: RequestConfig = {
  errorConfig: {
    adaptor: (res) => {
      return {
        ...res,
        success: res.ok,
        errorMessage: res.message,
        showType: 0,
      };
    },
  },
};
