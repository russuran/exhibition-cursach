import React from 'react';
import { Form, Input, Button } from 'antd';

const TicketForm = ({ initialValues, onSubmit }) => {
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
            <Form.Item name="exhibition_id" label="Exhibition ID" rules={[{ required: true }]}>
            <Input type="number" />
            </Form.Item>
            <Form.Item name="ticket_type" label="Ticket Type" rules={[{ required: true }]}>
                <Input />
            </Form.Item>
            <Form.Item name="date" label="Date" rules={[{ required: true }]}>
                <Input type="date" />
            </Form.Item>
            <Form.Item name="price" label="Price" rules={[{ required: true }]}>
                <Input type="number" />
            </Form.Item>
            <Form.Item name="payment_method" label="Payment Method" rules={[{ required: true }]}>
                <Input />
            </Form.Item>
            <Form.Item>
                <Button type="primary" htmlType="submit">
                    Submit
                </Button>
            </Form.Item>
        </Form>
    );
};

export default TicketForm;

