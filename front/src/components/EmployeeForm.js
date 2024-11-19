import React from 'react';
import { Form, Input, Button } from 'antd';

const EmployeeForm = ({ initialValues, onSubmit }) => {
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
            <Form.Item name="full_name" label="Full Name" rules={[{ required: true }]}>
                <Input />
            </Form.Item>
            <Form.Item name="position" label="Position" rules={[{ required: true }]}>
                <Input />
            </Form.Item>
            <Form.Item name="phone_number" label="Phone Number" rules={[{ required: true }]}>
                <Input type="number" />
            </Form.Item>
            <Form.Item name="salary" label="Salary" rules={[{ required: true }]}>
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

export default EmployeeForm;
