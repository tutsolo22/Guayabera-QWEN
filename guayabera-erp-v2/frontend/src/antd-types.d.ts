declare module 'antd' {
  export * from 'antd/lib';
}

// Declaraciones específicas para resolver problemas de tipos conocidos
declare module 'antd/lib/tag' {
  import { Tag } from 'antd';
  export default Tag;
}

declare module 'antd/lib/card' {
  import { Card } from 'antd';
  export default Card;
}

declare module 'antd/lib/space' {
  import { Space } from 'antd';
  export default Space;
}

declare module 'antd/lib/modal' {
  import { Modal } from 'antd';
  export default Modal;
}

declare module 'antd/lib/form' {
  import { Form } from 'antd';
  export default Form;
}

declare module 'antd/lib/input' {
  import { Input } from 'antd';
  export default Input;
}

declare module 'antd/lib/select' {
  import { Select } from 'antd';
  export default Select;
}

declare module 'antd/lib/button' {
  import { Button } from 'antd';
  export default Button;
}