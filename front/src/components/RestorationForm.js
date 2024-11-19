import React from 'react';
import { Form, Input, Button } from 'antd';

const RestorationForm = ({ initialValues, onSubmit }) => {
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
            <Form.Item name="employee_id" label="Employee ID" rules={[{ required: true }]}>
                <Input type="number" />
            </Form.Item>
            <Form.Item name="start_date" label="Start Date" rules={[{ required: true }]}>
                <Input type="date" />
            </Form.Item>
            <Form.Item name="end_date" label="End Date">
                <Input type="date" />
            </Form.Item>
            <Form.Item name="restoration_reason" label="Restoration Reason" rules={[{ required: true }]}>
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

export default RestorationForm;

