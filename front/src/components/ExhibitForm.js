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
        <Form form={form}
              onFinish={handleFinish}
              labelCol={{ span: 10 }}
              layout="vertical"
              style={{ maxWidth: 600 }}>
            <Form.Item name="title" label="Название" rules={[{ required: true, message: 'Пожалуйста, введите название'  }]}>
                <Input />
            </Form.Item>
            <Form.Item name="description" label="Описание" rules={[{ required: true, message: 'Пожалуйста, введите описание' }]}>
                <Input />
            </Form.Item>
            <Form.Item name="author" label="Автор" rules={[{ required: true, message: 'Пожалуйста, укажите автора' }]}>
                <Input />
            </Form.Item>
            <Form.Item name="year_created" label="Год создания" rules={[{ required: true, message: 'Пожалуйста, введите год создания' }]}>
                <Input type="number" />
            </Form.Item>
            <Form.Item name="country_of_origin" label="Страна происхождения" rules={[{ required: true, message: 'Пожалуйста, укажите страну происхождения' }]}>
                <Input />
            </Form.Item>
            <Form.Item name="material" label="Материал" rules={[{ required: true, message: 'Пожалуйста, укажите материал' }]}>
                <Input />
            </Form.Item>
            <Form.Item>
                <Button type="primary" htmlType="submit">
                    Сохранить
                </Button>
            </Form.Item>
        </Form>
    );
};

export default ExhibitForm;
