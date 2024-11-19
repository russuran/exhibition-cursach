import React from 'react';
import { Form, Input, Button } from 'antd';

const ExhibitForm = ({ initialValues, onSubmit }) => {
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
            <Form.Item name="title" label="Название" rules={[{ required: true }]}>
                <Input />
            </Form.Item>
            <Form.Item name="description" label="Описание" rules={[{ required: true }]}>
                <Input />
            </Form.Item>
            <Form.Item name="author" label="Автор" rules={[{ required: true }]}>
                <Input />
            </Form.Item>
            <Form.Item name="year_created" label="Год создания" rules={[{ required: true }]}>
                <Input type="number" />
            </Form.Item>
            <Form.Item name="country_of_origin" label="Страна происхождения" rules={[{ required: true }]}>
                <Input />
            </Form.Item>
            <Form.Item name="material" label="Материал" rules={[{ required: true }]}>
                <Input />
            </Form.Item>
            <Form.Item>
                <Button type="primary" htmlType="submit">
                    Создать
                </Button>
            </Form.Item>
        </Form>
    );
};

export default ExhibitForm;
