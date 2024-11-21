import React, { useEffect, useState } from 'react';
import { Table, Button, Modal, Form, Input } from 'antd';
import axios from 'axios';
import ExhibitForm from '../components/ExhibitForm';

const Exhibits = () => {
    const [exhibits, setExhibits] = useState([]);
    const [isModalVisible, setIsModalVisible] = useState(false);
    const [currentExhibit, setCurrentExhibit] = useState(null);

    useEffect(() => {
        fetchExhibits();
    }, []);

    const fetchExhibits = async () => {
        const response = await axios.get('http://localhost:5000/exhibits/');
        setExhibits(response.data);
    };

    const handleDelete = async (exhibitId) => {
        await axios.delete(`http://localhost:5000/exhibits/${exhibitId}`);
        fetchExhibits();
    };

    const handleModalOpen = (exhibit) => {
        setCurrentExhibit(exhibit);
        setIsModalVisible(true);
    };

    const handleModalClose = () => {
        setCurrentExhibit(null);
        setIsModalVisible(false);
    };

    const handleFormSubmit = async (values) => {
        if (currentExhibit) {
            await axios.put(`http://localhost:5000/exhibits/${currentExhibit.exhibit_id}`, values);
        } else {
            await axios.post('http://localhost:5000/exhibits/', values);
        }
        fetchExhibits();
        handleModalClose();
    };

    return (
        <div>
            <Button type="primary" onClick={() => handleModalOpen(null)} style={{ marginBottom: 16 }}>
                Добавить экспонат
            </Button>
            <Table dataSource={exhibits} rowKey="exhibit_id">
                <Table.Column title="Название" dataIndex="title" />
                <Table.Column title="Описание" dataIndex="description" />
                <Table.Column title="Автор" dataIndex="author" />
                <Table.Column title="Год создания" dataIndex="year_created" />
                <Table.Column title="Страна происхождения" dataIndex="country_of_origin" />
                <Table.Column title="Материал" dataIndex="material" />
                <Table.Column title="Действия" render={(text, exhibit) => (
                    <div style={{ display: 'flex', gap: '10px' }}>
                        <Button onClick={() => handleModalOpen(exhibit)}>Редактировать</Button>
                        <Button onClick={() => handleDelete(exhibit.exhibit_id)}>Удалить</Button>
                    </div>
                )} />
            </Table>
            <Modal
                title={currentExhibit ? "Редактировать экспонат" : "Добавить экспонат"}
                visible={isModalVisible}
                onCancel={handleModalClose}
                footer={null}
            >
                <ExhibitForm
                    initialValues={currentExhibit}
                    onSubmit={handleFormSubmit}
                />
            </Modal>
        </div>
    );
};

export default Exhibits;

