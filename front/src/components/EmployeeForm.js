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
        <Form 
            form={form} 
            onFinish={handleFinish} 
            labelCol={{ span: 10 }} 
            layout="vertical" 
            style={{ maxWidth: 600 }}
        >
            <Form.Item 
                name="full_name" 
                label="ФИО" 
                rules={[{ required: true, message: 'Пожалуйста, введите ФИО' }]}
            >
                <Input />
            </Form.Item>
            <Form.Item 
                name="position" 
                label="Должность" 
                rules={[{ required: true, message: 'Пожалуйста, введите должность' }]}
            >
                <Input />
            </Form.Item>
            <Form.Item 
                name="phone_number" 
                label="Номер телефона" 
                rules={[{ required: true, message: 'Пожалуйста, введите номер телефона' }]}
            >
                <Input type="number" />
            </Form.Item>
            <Form.Item 
                name="salary" 
                label="Заработная плата" 
                rules={[{ required: true, message: 'Пожалуйста, введите заработную плату' }]}
            >
                <Input type="number" />
            </Form.Item>
            <Form.Item>
                <Button type="primary" htmlType="submit">
                    Сохранить
                </Button>
            </Form.Item>
        </Form>
    );
};

export default EmployeeForm;
