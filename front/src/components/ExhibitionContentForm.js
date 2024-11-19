import React from 'react';
import { Form, Input, Button } from 'antd';

const ExhibitionContentForm = ({ initialValues, onSubmit }) => {
    const [form] = Form.useForm();

    React.useEffect(() => {
        if (initialValues) {
            form.setFieldsValue(initialValues);
        } else {
            form.resetFields();
        }
    }, [initialValues, form]);

    const handleFinish = (values) => {
        onSubmit(values);
    };

    return (
        <Form form={form} onFinish={handleFinish}>
            <Form.Item name="exhibit_id" label="Exhibit ID" rules={[{ required: true }]}>
                <Input type="number" />
            </Form.Item>
            <Form.Item name="exhibition_id" label="Exhibition ID" rules={[{ required: true }]}>
                <Input type="number" />
            </Form.Item>
            <Form.Item>
                <Button type="primary" htmlType="submit">
                    Submit
                </Button>
            </Form.Item>
        </Form>
    );
};

export default ExhibitionContentForm;
