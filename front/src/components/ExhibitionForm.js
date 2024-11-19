import React from 'react';
import { Form, Input, Button, DatePicker } from 'antd';
import moment from 'moment';

const ExhibitionForm = ({ initialValues, onSubmit }) => {
    const [form] = Form.useForm();

    React.useEffect(() => {
        if (initialValues) {
            form.setFieldsValue({
                ...initialValues,
                start_date: initialValues.start_date ? moment(initialValues.start_date) : null,
                end_date: initialValues.end_date ? moment(initialValues.end_date) : null,
            });
        } else {
            form.resetFields();
        }
    }, [initialValues, form]);

    const handleFinish = (values) => {
        onSubmit({
            ...values,
            start_date: values.start_date.format('YYYY-MM-DD'),
            end_date: values.end_date ? values.end_date.format('YYYY-MM-DD') : null,
        });
    };

    return (
        <Form form={form} onFinish={handleFinish}>
            <Form.Item name="employee_id" label="Employee ID" rules={[{ required: true }]}>
                <Input type="number" />
            </Form.Item>
            <Form.Item name="title" label="Title" rules={[{ required: true }]}>
                <Input />
            </Form.Item>
            <Form.Item name="description" label="Description" rules={[{ required: true }]}>
                <Input />
            </Form.Item>
            <Form.Item name="start_date" label="Start Date" rules={[{ required: true }]}>
                <DatePicker />
            </Form.Item>
            <Form.Item name="end_date" label="End Date">
                <DatePicker />
            </Form.Item>
            <Form.Item name="working_schedule" label="Working Schedule" rules={[{ required: true }]}>
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

export default ExhibitionForm;
