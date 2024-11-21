import React from 'react';
import { Form, Input, Button, Select, message } from 'antd';
import axios from 'axios';

const TicketForm = ({ initialValues, onSubmit }) => {
    const [form] = Form.useForm();
    const [exhibitions, setExhibitions] = React.useState([]);

    React.useEffect(() => {
        // Функция для получения данных с бэкенда
        const fetchExhibitions = async () => {
            try {
                const response = await axios.get('http://localhost:5000/exhibitions_list/');
                setExhibitions(response.data);
            } catch (error) {
                console.error('Ошибка при получении выставок:', error);
                message.error('Не удалось загрузить выставки. Пожалуйста, попробуйте позже.'); // User feedback
            }
        };

        fetchExhibitions();
    }, []);

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
                name="exhibition_id" 
                label="Выставка" 
                rules={[{ required: true, message: 'Пожалуйста, выберите выставку' }]}
            >
                <Select placeholder="Выберите выставку">
                    {exhibitions.map(exhibition => (
                        <Select.Option key={exhibition.id} value={exhibition.id}>
                            {exhibition.name}
                        </Select.Option>
                    ))}
                </Select>
            </Form.Item>
            <Form.Item 
                name="ticket_type" 
                label="Тип билета" 
                rules={[{ required: true, message: 'Пожалуйста, введите тип билета' }]}
            >
                <Input placeholder="Введите тип билета" />
            </Form.Item>
            <Form.Item 
                name="date" 
                label="Дата" 
                rules={[{ required: true, message: 'Пожалуйста, выберите дату' }]}
            >
                <Input type="date" />
            </Form.Item>
            <Form.Item 
                name="price" 
                label="Стоимость" 
                rules={[{ required: true, message: 'Пожалуйста, введите стоимость' }]}
            >
                <Input type="number" placeholder="Введите стоимость" />
            </Form.Item>
            <Form.Item 
                name="payment_method" 
                label="Способ оплаты" 
                rules={[{ required: true, message: 'Пожалуйста, введите способ оплаты' }]}
            >
                <Input placeholder="Введите способ оплаты" />
            </Form.Item>
            <Form.Item>
                <Button type="primary" htmlType="submit">
                    Сохранить
                </Button>
            </Form.Item>
        </Form>
    );
};

export default TicketForm;
